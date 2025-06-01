/battle/start/
{
    "characters": [
        {
            "id": "BP_Player_C_0",
            "name": "BP_Player_C_0",
            "type": "player",
            "traits": [
                "호전적"
            ],
            "skills": [
                "타격",
                "마비의 일격",
                "맹동 공격"
            ]
        },
        {
            "id": "BP_Player_C_1",
            "name": "BP_Player_C_1",
            "type": "player",
            "traits": [
                "호전적"
            ],
            "skills": [
                "타격",
                "마비의 일격",
                "맹동 공격",
                "취약 타격"
            ]
        },
        {
            "id": "BP_Player_C_2",
            "name": "BP_Player_C_2",
            "type": "player",
            "traits": [
                "호전적"
            ],
            "skills": [
                "타격",
                "마비의 일격",
                "맹동 공격",
                "취약 타격"
            ]
        },
        {
            "id": "BP_Player_C_3",
            "name": "BP_Player_C_3",
            "type": "player",
            "traits": [
                "호전적"
            ],
            "skills": [
                "타격",
                "마비의 일격",
                "맹동 공격",
                "취약 타격",
                "약화의 일격",
                "치명 일격",
                "파열 참격",
                "포효",
                "전투의 외침"
            ]
        },
        {
            "id": "BP_Enemy_C_0",
            "name": "BP_Enemy_C_0",
            "type": "monster",
            "traits": [
                "호전적"
            ],
            "skills": [
                "타격",
                "마비의 일격",
                "몸통 박치기",
                "맹동 공격",
                "취약 타격",
                "약화의 일격",
                "치명 일격"
            ]
        },
        {
            "id": "BP_Enemy_C_1",
            "name": "BP_Enemy_C_1",
            "type": "monster",
            "traits": [
                "호전적"
            ],
            "skills": [
                "타격",
                "마비의 일격",
                "몸통 박치기",
                "맹동 공격",
                "취약 타격",
                "약화의 일격"
            ]
        }
    ],
    "terrain": "desert",
    "weather": "sunny"
}


/battle/action/
{
    "cycle": 1,
    "turn": 5,
    "current_character_id": "BP_Enemy_C_1",
    "characters": [
        {
            "id": "BP_Player_C_0",
            "position": [ 4, 12 ],
            "hp": 100,
            "ap": 1,
            "mov": 5,
            "status_effects": []
        },
        {
            "id": "BP_Player_C_1",
            "position": [ 16, 18 ],
            "hp": 100,
            "ap": 1,
            "mov": 5,
            "status_effects": []
        },
        {
            "id": "BP_Player_C_2",
            "position": [ 8, 16 ],
            "hp": 100,
            "ap": 1,
            "mov": 5,
            "status_effects": []
        },
        {
            "id": "BP_Player_C_3",
            "position": [ 21, 2 ],
            "hp": 100,
            "ap": 1,
            "mov": 5,
            "status_effects": []
        },
        {
            "id": "BP_Enemy_C_0",
            "position": [ 14, 1 ],
            "hp": 80,
            "ap": 0,
            "mov": 5,
            "status_effects": []
        },
        {
            "id": "BP_Enemy_C_1",
            "position": [ 12, 5 ],
            "hp": 80,
            "ap": 10,
            "mov": 5,
            "status_effects": []
        }
    ]
}