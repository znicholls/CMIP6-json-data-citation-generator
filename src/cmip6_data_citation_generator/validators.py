from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError,
    RAISE,
)


def validate_dependent_fields(data, dependent_fields, name):
    error_msg = (
        "The fields {} in {} are co-dependent, if you supply one of them, you must "
        "supply all of them".format(dependent_fields, name)
    )
    if any([d in data for d in dependent_fields]):
        for field in dependent_fields:
            if field not in data:
                raise ValidationError(error_msg)


class NameIdentifierSchema(Schema):
    nameIdentifierScheme = fields.String(required=True)
    pid = fields.String(required=True)
    schemeURI = fields.Url(required=True)


class ContributorSchema(Schema):
    affiliation = fields.String()
    contributorName = fields.String(required=True)
    contributorType = fields.String(required=True)
    email = fields.String()
    familyName = fields.String()
    givenName = fields.String()
    nameIdentifier = fields.Nested(NameIdentifierSchema)

    @validates_schema
    def dependency_validation(self, data):
        validate_dependent_fields(
            data, ["email", "familyName", "givenName"], "contributors"
        )


class CreatorSchema(Schema):
    affiliation = fields.String()
    creatorName = fields.String(required=True)
    email = fields.String()
    familyName = fields.String()
    givenName = fields.String()
    nameIdentifier = fields.Nested(NameIdentifierSchema)

    @validates_schema
    def dependency_validation(self, data):
        validate_dependent_fields(
            data, ["email", "familyName", "givenName"], "creators"
        )


class FundingReferencesSchema(Schema):
    funderName = fields.String(required=True)
    funderIdentifier = fields.String()
    funderIdentifierType = fields.String()

    @validates_schema
    def dependency_validation(self, data):
        validate_dependent_fields(
            data, ["funderIdentifier", "funderIdentifierType"], "fundingReferences"
        )


class RelatedIdentifiersSchema(Schema):
    relatedIdentifier = fields.String(required=True)
    relatedIdentifierType = fields.String(required=True)
    relationType = fields.String(required=True)


class SubjectsSchema(Schema):
    subject = fields.String(required=True)
    schemeURI = fields.Url()
    subjectScheme = fields.String()

    @validates_schema
    def dependency_validation(self, data):
        validate_dependent_fields(data, ["schemeURI", "subjectScheme"], "subjects")


class CitationSchema(Schema):
    class Meta:
        unknown = RAISE

    contributors = fields.Nested(ContributorSchema, required=True, many=True)
    creators = fields.Nested(CreatorSchema, required=True, many=True)
    fundingReferences = fields.Nested(FundingReferencesSchema, many=True)
    relatedIdentifiers = fields.Nested(RelatedIdentifiersSchema, many=True)
    subjects = fields.Nested(SubjectsSchema, required=True, many=True)
    titles = fields.List(fields.String(), required=True)

    @validates("subjects")
    def validate_subjects(self, value):
        subject_compulsory_dict = {
            "subject": "<subject>",
            "subjectScheme": "DRS",
            "schemeURI": "http://github.com/WCRP-CMIP/CMIP6_CVs",
        }
        if value[0] != subject_compulsory_dict:
            error_msg = (
                "^The first element under subjects should be autofilled by the "
                "generator and hence be equal to {}".format(subject_compulsory_dict)
            )
            raise ValidationError(error_msg)
