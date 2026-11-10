from db import Prisma

PENDING_STATUS= {
        "identity":"c7d0f15e-fd4b-43ea-9d1f-3827a8871947",
        "name":"pending",
        "description":"order payment is pending",
        "icon_name":"clock",
        "badge_color":"yellow"
    }
    
PAID_STATUS= {
            "identity":"f8e38f54-3b8e-4d1e-9c8a-57f8e3d16b20",
            "name":"paid",
            "description":"order payment has be completed successfully",
            "icon_name":"check-circle",
            "badge_color":"green"
        }


status = [
    PENDING_STATUS,
    PAID_STATUS,
]


async def seed_status():
    for single_status in status:
        seeded_status = await Prisma.client_order_status.upsert(
            where={
                "identity": single_status["identity"],
            },
            data={
                "create": {
                    "identity": single_status["identity"],
                    "name": single_status["name"],
                    "description": single_status["description"],
                    "icon_name": single_status["icon_name"],
                    "badge_color": single_status["badge_color"],
                },
                "update": {
                    "name": single_status["name"],
                    "description": single_status["description"],
                    "icon_name": single_status["icon_name"],
                    "badge_color": single_status["badge_color"],
                },
            },
        )

        print("seed status", seeded_status)