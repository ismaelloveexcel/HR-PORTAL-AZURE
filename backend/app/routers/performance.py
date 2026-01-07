from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.auth.dependencies import require_auth, require_hr
from app.models.employee import Employee
from app.schemas.performance import (
    PerformanceCycleCreate, PerformanceCycleUpdate, PerformanceCycleResponse,
    PerformanceReviewCreate, PerformanceReviewResponse,
    SelfAssessmentSubmit, ManagerReviewSubmit,
    BulkReviewCreate, PerformanceStats
)
from app.services.performance_service import performance_service

router = APIRouter(prefix="/performance", tags=["Performance Management"])


@router.get("/cycles", response_model=List[PerformanceCycleResponse])
async def list_cycles(
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    cycles = await performance_service.get_cycles(db, status)
    result = []
    for cycle in cycles:
        stats = await performance_service.get_cycle_stats(db, cycle.id)
        result.append({
            "id": cycle.id,
            "name": cycle.name,
            "cycle_type": cycle.cycle_type,
            "start_date": cycle.start_date,
            "end_date": cycle.end_date,
            "self_assessment_deadline": cycle.self_assessment_deadline,
            "manager_review_deadline": cycle.manager_review_deadline,
            "status": cycle.status,
            "created_at": cycle.created_at,
            "review_count": stats["total_reviews"]
        })
    return result


@router.post("/cycles", response_model=PerformanceCycleResponse)
async def create_cycle(
    data: PerformanceCycleCreate,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_hr)
):
    cycle = await performance_service.create_cycle(db, data, current_user.employee_id)
    return {
        "id": cycle.id,
        "name": cycle.name,
        "cycle_type": cycle.cycle_type,
        "start_date": cycle.start_date,
        "end_date": cycle.end_date,
        "self_assessment_deadline": cycle.self_assessment_deadline,
        "manager_review_deadline": cycle.manager_review_deadline,
        "status": cycle.status,
        "created_at": cycle.created_at,
        "review_count": 0
    }


@router.get("/cycles/{cycle_id}", response_model=PerformanceCycleResponse)
async def get_cycle(
    cycle_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    cycle = await performance_service.get_cycle(db, cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    stats = await performance_service.get_cycle_stats(db, cycle_id)
    return {
        "id": cycle.id,
        "name": cycle.name,
        "cycle_type": cycle.cycle_type,
        "start_date": cycle.start_date,
        "end_date": cycle.end_date,
        "self_assessment_deadline": cycle.self_assessment_deadline,
        "manager_review_deadline": cycle.manager_review_deadline,
        "status": cycle.status,
        "created_at": cycle.created_at,
        "review_count": stats["total_reviews"]
    }


@router.put("/cycles/{cycle_id}", response_model=PerformanceCycleResponse)
async def update_cycle(
    cycle_id: int,
    data: PerformanceCycleUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_hr)
):
    cycle = await performance_service.update_cycle(db, cycle_id, data)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    stats = await performance_service.get_cycle_stats(db, cycle_id)
    return {
        "id": cycle.id,
        "name": cycle.name,
        "cycle_type": cycle.cycle_type,
        "start_date": cycle.start_date,
        "end_date": cycle.end_date,
        "self_assessment_deadline": cycle.self_assessment_deadline,
        "manager_review_deadline": cycle.manager_review_deadline,
        "status": cycle.status,
        "created_at": cycle.created_at,
        "review_count": stats["total_reviews"]
    }


@router.get("/cycles/{cycle_id}/stats", response_model=PerformanceStats)
async def get_cycle_stats(
    cycle_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    stats = await performance_service.get_cycle_stats(db, cycle_id)
    return stats


@router.get("/reviews", response_model=List[PerformanceReviewResponse])
async def list_reviews(
    cycle_id: Optional[int] = Query(None),
    employee_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    reviews = await performance_service.get_reviews(db, cycle_id, employee_id, status=status)
    return reviews


@router.post("/reviews", response_model=PerformanceReviewResponse)
async def create_review(
    data: PerformanceReviewCreate,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_hr)
):
    review = await performance_service.create_review(db, data)
    return await performance_service.get_review(db, review.id)


@router.post("/reviews/bulk")
async def create_bulk_reviews(
    data: BulkReviewCreate,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_hr)
):
    reviews = await performance_service.create_bulk_reviews(db, data)
    return {"created": len(reviews)}


@router.get("/reviews/{review_id}", response_model=PerformanceReviewResponse)
async def get_review(
    review_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    review = await performance_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/reviews/{review_id}/self-assessment")
async def submit_self_assessment(
    review_id: int,
    data: SelfAssessmentSubmit,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    review = await performance_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review["employee_id"] != current_user.id and current_user.role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated = await performance_service.submit_self_assessment(db, review_id, data)
    return {"status": "submitted", "review_id": updated.id}


@router.post("/reviews/{review_id}/manager-review")
async def submit_manager_review(
    review_id: int,
    data: ManagerReviewSubmit,
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    review = await performance_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review["reviewer_id"] != current_user.id and current_user.role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated = await performance_service.submit_manager_review(db, review_id, data)
    return {"status": "completed", "review_id": updated.id}


@router.get("/my-reviews", response_model=List[PerformanceReviewResponse])
async def get_my_reviews(
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    reviews = await performance_service.get_employee_reviews(db, current_user.id)
    return reviews


@router.get("/team-reviews", response_model=List[PerformanceReviewResponse])
async def get_team_reviews(
    db: AsyncSession = Depends(get_session),
    current_user: Employee = Depends(require_auth)
):
    reviews = await performance_service.get_manager_reviews(db, current_user.id)
    return reviews
