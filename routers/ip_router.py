from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPAuthorizationCredentials
from models.models import SuspiciousIp
import schemas.ip as ip_schema
from routers import security
from routers.user_auth import get_current_active_user
from schemas.user_auth import User
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/report-ip/', response_model=ip_schema.ResReportIp)
async def report_ip(report_ip: ip_schema.ReqReportIp,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    suspicious_ip = SuspiciousIp.insert(ip_address=report_ip.ip_address, db=db)
    return suspicious_ip


@router.get('/query-ip/', response_model=ip_schema.ResQueryIp)
async def query_ip(ip_address: str | None = Query(None, pattern=ip_schema.regex),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_user)):
    try:
        suspicious_ip = db.query(SuspiciousIp).filter(SuspiciousIp.ip_address == ip_address).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="server error: database")
    if not suspicious_ip:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ip does not exist")
    return suspicious_ip
