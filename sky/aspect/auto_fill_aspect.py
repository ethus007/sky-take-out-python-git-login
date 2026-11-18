# 对应 Java: com.sky.aspect.AutoFillAspect
from datetime import datetime

from sky.constant.auto_fill_constant import AutoFillConstant
from sky.context.base_context import BaseContext
from sky.enumeration.operation_type import OperationType


class AutoFillAspect:
    @staticmethod
    def autoFill(entity, operationType: OperationType) -> None:
        now = datetime.now()
        current_id = BaseContext.getCurrentId()
        if operationType == OperationType.INSERT:
            setattr(entity, AutoFillConstant.SET_CREATE_TIME, now)
            setattr(entity, AutoFillConstant.SET_CREATE_USER, current_id)
            setattr(entity, AutoFillConstant.SET_UPDATE_TIME, now)
            setattr(entity, AutoFillConstant.SET_UPDATE_USER, current_id)
        elif operationType == OperationType.UPDATE:
            setattr(entity, AutoFillConstant.SET_UPDATE_TIME, now)
            setattr(entity, AutoFillConstant.SET_UPDATE_USER, current_id)
