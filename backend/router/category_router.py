from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.category_service import get_categories_service

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    )

class Category(BaseModel):
    id: int
    name: str
    description: str

@router.get("/get_categories/{site_id}")
def get_categories(site_id: int):
    result = get_categories_service(site_id)
    return result



''' "sites": """
            CREATE TABLE IF NOT EXISTS `sites` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(100) NOT NULL,
                `logo_url` VARCHAR(255),
                `description` TEXT,
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        "categories": """
            CREATE TABLE IF NOT EXISTS `categories` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(50) NOT NULL UNIQUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵SITE_CATEGORIES
        "site_categories": """
            CREATE TABLE IF NOT EXISTS `site_categories` (
                `site_id` INT NOT NULL,
                `category_id` INT NOT NULL,
                PRIMARY KEY (`site_id`, `category_id`),
                FOREIGN KEY (`site_id`) REFERENCES `sites` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,'''