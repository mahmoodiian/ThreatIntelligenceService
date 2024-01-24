from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String, DateTime
from settings.database import Base


class SuspiciousIp(Base):
    __tablename__ = 'suspicious_ip'
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True, unique=True)
    report_count = Column(Integer, default=1)
    last_report_time = Column(DateTime, default=datetime.now())

    @staticmethod
    def insert(ip_address, db):
        try:
            suspicious_ip = db.query(SuspiciousIp).filter(SuspiciousIp.ip_address == ip_address).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="server error: database")
        if suspicious_ip:
            suspicious_ip.report_count += 1
            suspicious_ip.last_report_time = datetime.now()
            db.commit()
            db.refresh(suspicious_ip)
        else:
            suspicious_ip = SuspiciousIp(
                ip_address=ip_address
            )
            db.add(suspicious_ip)
            db.commit()
            db.refresh(suspicious_ip)

        return suspicious_ip
