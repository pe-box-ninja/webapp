from typing import List, Dict, Tuple
import random
import math

from app.lib.courier_service import a_star_route_optimization


class Address:
    def __init__(self, address: str, lat: float, lon: float):
        self.address = address
        self.lat = lat
        self.lon = lon


# Predefined list of Veszprém addresses with approximate coordinates
VESZPREM_ADDRESSES = [
    Address("Egyetem utca 1.", 47.089400, 17.907501),
    Address("Óváros tér 9.", 47.0931, 17.9064),
    Address("Kossuth Lajos utca 21.", 47.0927, 17.9098),
    Address("Wartha Vince utca 1.", 47.0909, 17.9057),
    Address("Jeszenák utca 3.", 47.0894, 17.9005),
    Address("Déli intézményközpont", 47.0871, 17.9048),
    Address("Veszprémi Állatkert", 47.0905, 17.8980),
    Address("Füredi utca 11.", 47.0972, 17.9173),
    Address("Cholnoky Jenő utca 22.", 47.0942, 17.9208),
    Address("Haszkovó utca 18.", 47.1012, 17.9095),
]


def distance(addr1: Address, addr2: Address) -> float:
    # Using Haversine formula for more accurate distance calculation
    R = 6371  # Earth's radius in kilometers

    lat1, lon1 = math.radians(addr1.lat), math.radians(addr1.lon)
    lat2, lon2 = math.radians(addr2.lat), math.radians(addr2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in kilometers


def nearest_neighbor_tsp(addresses: List[Address]) -> Tuple[List[Address], List[Dict]]:
    start = addresses[0]
    unvisited = addresses.copy()
    path = [start]
    total_distance = 0
    steps = []

    while unvisited:
        last = path[-1]
        distances = [(addr, distance(last, addr)) for addr in unvisited]
        next_addr, min_distance = min(distances, key=lambda x: x[1])

        path.append(next_addr)
        unvisited.remove(next_addr)
        total_distance += min_distance

        steps.append(
            {
                "current": last.address,
                "options": [
                    {"address": addr.address, "distance": dist}
                    for addr, dist in distances
                ],
                "chosen": next_addr.address,
                "distance": min_distance,
                "total_distance": total_distance,
            }
        )

    return path, steps


def simulate_delivery_old() -> Dict:
    selected_addresses = random.sample(VESZPREM_ADDRESSES, 7)
    optimal_route, steps = nearest_neighbor_tsp(selected_addresses, 0)

    return {
        "addresses": [
            {
                "address": addr.address,
                "lat": addr.lat,
                "lon": addr.lon,
            }
            for addr in selected_addresses
        ],
        "optimal_route": [
            {
                "address": addr.address,
                "lat": addr.lat,
                "lon": addr.lon,
            }
            for addr in optimal_route
        ],
        "steps": steps,
    }


def simulate_delivery() -> Dict:
    selected_addresses = random.sample(VESZPREM_ADDRESSES, len(VESZPREM_ADDRESSES))

    # Convert
    addresses_for_a_star = [
        {
            "address": addr.address,
            "lat": addr.lat,
            "lon": addr.lon,
        }
        for addr in selected_addresses
    ]
    optimal_route, steps = a_star_route_optimization(
        addresses_for_a_star, start_index=0
    )
    return {
        "addresses": addresses_for_a_star,
        "optimal_route": optimal_route,
        "steps": steps,
    }
