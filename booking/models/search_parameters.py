from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, date


class SearchParameters(BaseModel):
    city: str = Field(..., description="Destination city name")
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    num_adults: int = Field(1, ge=1, description="Number of adults")
    num_children: int = Field(0, ge=0, description="Number of children")
    children_ages: List[int] = Field(default_factory=list, description="Ages of children")
    currency: Optional[str] = Field(None, description="Currency code (e.g., 'USD', 'EUR')")
    
model_config = {
        "validate_assignment": True,
        "extra": "forbid",
    }
    
@field_validator('check_in_date', 'check_out_date')
@classmethod
def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError(f"Date '{v}' is not in YYYY-MM-DD format")
    
@field_validator('check_in_date')
@classmethod
def validate_not_in_past(cls, v: str) -> str:
        check_in = datetime.strptime(v, '%Y-%m-%d').date()
        today = date.today()
        if check_in < today:
            raise ValueError("Check-in date cannot be in the past")
        return v
    
@field_validator('children_ages')
@classmethod
def validate_children_ages(cls, v: List[int], info) -> List[int]:
        for age in v:
            if not 0 <= age <= 17:
                raise ValueError(f"Child age {age} must be between 0 and 17")
        return v
    
@field_validator('currency')
@classmethod
def validate_currency(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not isinstance(v, str) or len(v) != 3:
                raise ValueError("Currency code must be a 3-letter code")
            return v.upper()
        return v
    
@model_validator(mode='after')
def validate_checkout_after_checkin(self) -> 'SearchParameters':
        check_in = datetime.strptime(self.check_in_date, '%Y-%m-%d')
        check_out = datetime.strptime(self.check_out_date, '%Y-%m-%d')
        if check_out <= check_in:
            raise ValueError("Check-out date must be after check-in date")
        return self
    
@model_validator(mode='after')
def validate_children_count(self) -> 'SearchParameters':
        if len(self.children_ages) != self.num_children:
            raise ValueError(
                f"Number of ages provided ({len(self.children_ages)}) doesn't match "
                f"number of children ({self.num_children})"
            )
        return self