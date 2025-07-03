
from app.models.clinical_trials import ClinicalTrials
from app.models.trial_consent_Information import TrialConsentInformation

from app import db


class ClinicalTrialService:

    @staticmethod
    def createClinicalTrial(data, organization_id, researcher_id):
        clinicaltrial = ClinicalTrials(
            title=data['title'],
            organization_id=organization_id,
            createdByResearcher_id=researcher_id,
            overview=data['overview'],
            participation_criteria=data['participation_criteria'],
            visit_details=data['visit_details'],
            status="active"
        )

        db.session.add(clinicaltrial)
        db.session.flush() 

        return clinicaltrial

    @staticmethod
    def createClinicalTrialsConsent(data, clinical_trial_id):
        consentInformation = TrialConsentInformation(
            clinical_trial_id=clinical_trial_id,
            risks=data['risks'],
            benefits=data['benefits'],
            privacy=data['privacy'],
            compensation="compensation",
            rights=data['rights'],
            safety_contacts=data['safety_contacts'],
            ethics=data['ethics'],
            consent_understanding=data['consent_understanding'],
        )

        db.session.add(consentInformation)

        return consentInformation
    
    
