import os
import time
import json
import fcntl
import requests
import threading

DELETIONS_FILE = "/opt/trading_agent/pending_deletions.jsonl"
DEFAULT_TTL = 86400  # 24 hours (1 day)

def record_for_auto_delete(chat_id, message_id, ttl_seconds=DEFAULT_TTL, timestamp=None):
    """Atomically append a message record to the deletion queue with individual TTL."""
    if not message_id or not chat_id:
        return
    if timestamp is None:
        timestamp = time.time()
    
    record = {
        "chat_id": chat_id,
        "message_id": message_id,
        "time": timestamp,
        "ttl": ttl_seconds,
        "expire_at": timestamp + ttl_seconds
    }
    line = json.dumps(record) + "\n"
    
    try:
        os.makedirs(os.path.dirname(DELETIONS_FILE), exist_ok=True)
        with open(DELETIONS_FILE, "a", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.write(line)
                f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except Exception as e:
        print(f"[!] Error recording message for auto-delete: {e}")

def delete_single_message(bot_token, chat_id, message_id):
    """Calls Telegram deleteMessage API."""
    if not bot_token or not chat_id or not message_id:
        return False, "invalid_params"
    url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "message_id": message_id}, timeout=10)
        res = r.json()
        if res.get("ok"):
            return True, "deleted"
        err_desc = res.get("description", "")
        # If message not found or already deleted, consider resolved
        if "not found" in err_desc.lower() or "can't be deleted" in err_desc.lower():
            return True, f"skipped ({err_desc})"
        if res.get("error_code") == 429:
            return False, "rate_limited"
        return False, err_desc
    except Exception as e:
        return False, str(e)

def delete_message_now(bot_token, chat_id, message_id):
    """Immediately delete a message and remove it from the pending deletions file."""
    if not message_id or not chat_id:
        return
    
    # 1. Call API to delete
    success, reason = delete_single_message(bot_token, chat_id, message_id)
    print(f"[AutoDelete:Instant] Purged msg {message_id} (Status: {reason})")
    
    # 2. Clean from pending file if exists
    if os.path.exists(DELETIONS_FILE):
        try:
            with open(DELETIONS_FILE, "r+", encoding="utf-8") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    lines = f.readlines()
                    remaining = []
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                            if rec.get("chat_id") == chat_id and rec.get("message_id") == message_id:
                                continue  # remove
                            remaining.append(rec)
                        except Exception:
                            continue
                    f.seek(0)
                    f.truncate()
                    for rec in remaining:
                        f.write(json.dumps(rec) + "\n")
                    f.flush()
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as e:
            print(f"[!] Error removing msg {message_id} from queue file: {e}")

def delete_message_after(bot_token, chat_id, message_id, delay_seconds=5.0):
    """Schedules an immediate, accurate timed deletion using a lightweight thread timer."""
    if not message_id or not chat_id:
        return
    t = threading.Timer(delay_seconds, delete_message_now, args=[bot_token, chat_id, message_id])
    t.daemon = True
    t.start()
    return t

def purge_expired_messages(bot_token, default_ttl=DEFAULT_TTL):
    """Purge messages older than their individual expire_at timestamp with process-safe locking."""
    if not os.path.exists(DELETIONS_FILE):
        return 0
    
    now = time.time()
    deleted_count = 0
    
    try:
        with open(DELETIONS_FILE, "r+", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                lines = f.readlines()
                remaining_records = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    
                    expire_at = rec.get("expire_at")
                    if expire_at is None:
                        expire_at = rec.get("time", now) + rec.get("ttl", default_ttl)
                    
                    if now >= expire_at:
                        success, reason = delete_single_message(bot_token, rec["chat_id"], rec["message_id"])
                        if success:
                            deleted_count += 1
                            age = int(now - rec.get("time", now))
                            print(f"[AutoDelete] Purged msg {rec['message_id']} (Age: {age}s, Status: {reason})")
                            time.sleep(0.05)  # gentle pacing
                        else:
                            if reason == "rate_limited":
                                print("[AutoDelete] Hit Telegram rate limit, will retry remaining next cycle")
                                remaining_records.append(rec)
                                break
                            else:
                                remaining_records.append(rec)
                    else:
                        remaining_records.append(rec)
                
                # Rewrite active records
                f.seek(0)
                f.truncate()
                for rec in remaining_records:
                    f.write(json.dumps(rec) + "\n")
                f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except Exception as e:
        print(f"[!] Error during purge_expired_messages: {e}")
        
    return deleted_count

def get_queue_stats(default_ttl=DEFAULT_TTL, ttl_seconds=None):
    """Returns queue statistics for reporting."""
    if ttl_seconds is not None:
        default_ttl = ttl_seconds
    if not os.path.exists(DELETIONS_FILE):
        return {"total": 0, "oldest_age": 0, "next_deletion_in": None}
    
    now = time.time()
    total = 0
    oldest_time = None
    next_expire = None
    
    try:
        with open(DELETIONS_FILE, "r", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        total += 1
                        t = rec.get("time", now)
                        if oldest_time is None or t < oldest_time:
                            oldest_time = t
                        
                        exp = rec.get("expire_at")
                        if exp is None:
                            exp = t + rec.get("ttl", default_ttl)
                        
                        if next_expire is None or exp < next_expire:
                            next_expire = exp
                    except Exception:
                        pass
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except Exception:
        pass
        
    oldest_age = (now - oldest_time) if oldest_time else 0
    next_del = max(0, next_expire - now) if next_expire else None
    return {
        "total": total,
        "oldest_age": int(oldest_age),
        "next_deletion_in": int(next_del) if next_del is not None else None
    }

def start_auto_delete_worker(bot_token, check_interval=60, default_ttl=DEFAULT_TTL, ttl_seconds=None):
    """Starts the auto delete background daemon thread."""
    if ttl_seconds is not None:
        default_ttl = ttl_seconds
    def worker():
        print(f"[*] Multi-tier auto-delete daemon active (default TTL: {default_ttl//3600}h).")
        while True:
            try:
                purge_expired_messages(bot_token, default_ttl)
            except Exception as e:
                print(f"[!] Auto-delete worker error: {e}")
            time.sleep(check_interval)
            
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t
