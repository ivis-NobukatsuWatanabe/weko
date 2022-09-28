from marshmallow import Schema, fields 
from marshmallow.validate import Range

class ActivitySchema(Schema):
    workflow_id = fields.Integer(required=True)
    flow_id = fields.Integer(required=True)
    itemtype_id = fields.Integer(allow_none=True)
    extra_info = fields.Dict(allow_none=True)
    related_title = fields.String(allow_none=True)
    activity_confirm_term_of_use = fields.Boolean(allow_none=True)
    activity_login_user= fields.Integer(allow_none=True)
    activity_update_user= fields.Integer(allow_none=True)
    class Meta:
        strict = True

class LockedValueSchema(Schema):
    locked_value = fields.String(required=True)
    class Meta:
        strict = True

class ResponseSchema(Schema):
    code = fields.Integer(required=True,validate=Range(min=-2,max=1))
    msg = fields.String(required=True)
    class Meta:
        strict = True

class ResponseMessageSchema(ResponseSchema):
    data = fields.Dict(allow_none=True)
    
class ResponseUnlockSchema(Schema):
    code = fields.Integer(required=True)
    msg = fields.String()
    class Meta:
        strict = True
        
class GetFeedbackMailListSchema(ResponseSchema):
    data = fields.List(fields.Dict(),allow_none=True)    
    
class SaveActivitySchema(Schema):
    activity_id = fields.String(required=True)
    title = fields.String(required=True)
    shared_user_id = fields.Integer(required=True,validate=Range(min=-1))
    approval1 = fields.String(allow_none=True)
    approval2 = fields.String(allow_none=True)
    class Meta:
        strict = True

class CheckApprovalSchema(Schema):
    check_handle = fields.Integer(required=True,validate=Range(min=-1,max=1))
    check_continue = fields.Integer(required=True,validate=Range(min=-1,max=1))
    error = fields.Integer(required=True,validate=Range(min=-1,max=1))
    class Meta:
        strict = True

class SaveActivityResponseSchema(Schema):
    success = fields.Boolean(required=True)
    msg = fields.String(required=True)
    class Meta:
        strict = True