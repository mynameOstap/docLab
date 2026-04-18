from ..extensions import db
from ..models.consultant import Consultant


class ConsultantService:
    @staticmethod
    def get_all():
        return Consultant.query.order_by(Consultant.id.desc()).all()

    @staticmethod
    def get_by_id(consultant_id: int):
        return Consultant.query.get_or_404(consultant_id)

    @staticmethod
    def create(data: dict):
        consultant = Consultant(**data)
        db.session.add(consultant)
        db.session.commit()
        return consultant

    @staticmethod
    def update(consultant: Consultant, data: dict):
        for key, value in data.items():
            setattr(consultant, key, value)
        db.session.commit()
        return consultant

    @staticmethod
    def delete(consultant: Consultant):
        db.session.delete(consultant)
        db.session.commit()
