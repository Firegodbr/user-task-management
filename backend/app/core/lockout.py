"""
Account Lockout Management

Handles failed login attempt tracking and account locking.
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.login_attempts import LoginAttempt
from app.core.audit import AuditLogger
from loguru import logger

# Configuration
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30


async def record_login_attempt(
    db: AsyncSession,
    username: str,
    success: bool,
    ip_address: str = None
) -> None:
    """
    Record a login attempt in the database.

    Args:
        db: Database session
        username: Username attempted
        success: Whether the login succeeded
        ip_address: IP address of the attempt
    """
    attempt = LoginAttempt(
        username=username,
        success=1 if success else 0,
        ip_address=ip_address,
        attempted_at=datetime.now(timezone.utc)
    )
    db.add(attempt)
    await db.commit()


async def handle_failed_login(db: AsyncSession, user: User, ip_address: str = "unknown") -> None:
    """
    Handle a failed login attempt. Increment counter and lock if needed.

    Args:
        db: Database session
        user: User model instance
        ip_address: IP address of the failed attempt
    """
    user.failed_login_attempts += 1

    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        logger.warning(
            f"Account locked for user {user.username} due to {user.failed_login_attempts} failed attempts. "
            f"Locked until {user.locked_until}"
        )
        # Audit log
        AuditLogger.account_locked(user.username, ip_address, user.failed_login_attempts)

    await db.commit()


async def handle_successful_login(db: AsyncSession, user: User) -> None:
    """
    Handle a successful login. Reset failed attempt counter.

    Args:
        db: Database session
        user: User model instance
    """
    was_locked = user.locked_until is not None
    user.failed_login_attempts = 0
    user.locked_until = None

    if was_locked:
        # Audit log account unlock
        AuditLogger.account_unlocked(user.username, method="successful_login")

    await db.commit()


async def check_account_locked(user: User) -> tuple[bool, str]:
    """
    Check if an account is locked.

    Args:
        user: User model instance

    Returns:
        Tuple of (is_locked, message)
    """
    if user.is_locked():
        locked_until = user.locked_until
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)

        remaining = locked_until - datetime.now(timezone.utc)
        minutes_remaining = int(remaining.total_seconds() / 60)

        message = (
            f"Account is locked due to too many failed login attempts. "
            f"Please try again in {minutes_remaining} minutes."
        )
        return True, message

    return False, ""


async def cleanup_old_login_attempts(db: AsyncSession, days: int = 30) -> int:
    """
    Clean up old login attempt records.

    Args:
        db: Database session
        days: Delete records older than this many days

    Returns:
        Number of records deleted
    """
    from sqlalchemy import delete
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    result = await db.execute(
        delete(LoginAttempt).where(LoginAttempt.attempted_at < cutoff_date)
    )
    await db.commit()

    deleted_count = result.rowcount
    if deleted_count > 0:
        logger.info(f"Cleaned up {deleted_count} old login attempt records")

    return deleted_count
