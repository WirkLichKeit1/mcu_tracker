"""
MCU Seed — Ordem Cronológica Completa
Run: docker compose exec api python -m app.seed
"""

from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.models import Content, ContentType, Era, Marathon, MarathonItem, Universe


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

UNIVERSE = {
    "name": "Marvel Cinematic Universe",
    "slug": "mcu",
    "description": "O universo cinematográfico da Marvel, desde a Segunda Guerra até o Multiverso.",
}

MARATHON = {
    "name": "MCU — Ordem Cronológica",
    "description": "Todos os filmes, séries, especiais e one-shots em ordem cronológica dos eventos no universo.",
}

# Each era: (name, position)
ERAS: list[tuple[str, int]] = [
    ("Era da Segunda Guerra e Pós-Guerra", 1),
    ("Década de 1990", 2),
    ("Início da Era dos Heróis", 3),
    ("Pós-Batalha de Nova York", 4),
    ("Expansão Cósmica", 5),
    ("Ascensão dos Vigilantes de Rua", 6),
    ("Era de Ultron", 7),
    ("Guerra Civil", 8),
    ("Ragnarok e o Fim da Saga do Infinito", 9),
    ("O Blip e o Retorno", 10),
    ("Saga do Multiverso", 11),
    ("Multiverso / Realidades Paralelas (opcional)", 12),
]

# Each content: (title, type, release_date, runtime_minutes)
CONTENTS: list[tuple[str, ContentType, str | None, int | None]] = [
    # Era 1 — Segunda Guerra e Pós-Guerra
    ("Captain America: The First Avenger", ContentType.movie, "2011-07-22", 124),
    ("Agent Carter", ContentType.special, "2013-09-03", 15),
    ("Agent Carter – Temporada 1", ContentType.series, "2015-01-06", 480),
    ("Agent Carter – Temporada 2", ContentType.series, "2016-01-19", 440),
    # Era 2 — Década de 1990
    ("Captain Marvel", ContentType.movie, "2019-03-08", 124),
    # Era 3 — Início da Era dos Heróis
    ("Iron Man", ContentType.movie, "2008-05-02", 126),
    ("Iron Man 2", ContentType.movie, "2010-05-07", 124),
    ("The Incredible Hulk", ContentType.movie, "2008-06-13", 112),
    ("The Consultant", ContentType.one_shot, "2011-09-13", 4),
    ("A Funny Thing Happened on the Way to Thor's Hammer", ContentType.one_shot, "2011-09-13", 4),
    ("Thor", ContentType.movie, "2011-05-06", 115),
    ("The Avengers", ContentType.movie, "2012-05-04", 143),
    ("Item 47", ContentType.one_shot, "2012-09-25", 12),
    # Era 4 — Pós-Batalha de Nova York
    ("Iron Man 3", ContentType.movie, "2013-05-03", 130),
    ("All Hail the King", ContentType.one_shot, "2014-02-04", 14),
    ("Agents of S.H.I.E.L.D. – Temporada 1", ContentType.series, "2013-09-24", 990),
    ("Thor: The Dark World", ContentType.movie, "2013-11-08", 112),
    ("Captain America: The Winter Soldier", ContentType.movie, "2014-04-04", 136),
    ("Agents of S.H.I.E.L.D. – Temporada 2", ContentType.series, "2014-09-23", 990),
    # Era 5 — Expansão Cósmica
    ("Guardians of the Galaxy", ContentType.movie, "2014-08-01", 121),
    ("Guardians of the Galaxy Vol. 2", ContentType.movie, "2017-05-05", 136),
    # Era 6 — Ascensão dos Vigilantes de Rua
    ("Daredevil – Temporada 1", ContentType.series, "2015-04-10", 780),
    ("Jessica Jones – Temporada 1", ContentType.series, "2015-11-20", 676),
    # Era 7 — Era de Ultron
    ("Avengers: Age of Ultron", ContentType.movie, "2015-05-01", 141),
    ("Ant-Man", ContentType.movie, "2015-07-17", 117),
    ("Daredevil – Temporada 2", ContentType.series, "2016-03-18", 676),
    ("Luke Cage – Temporada 1", ContentType.series, "2016-09-30", 676),
    ("Agents of S.H.I.E.L.D. – Temporada 3", ContentType.series, "2015-09-29", 990),
    # Era 8 — Guerra Civil
    ("Captain America: Civil War", ContentType.movie, "2016-05-06", 147),
    ("Black Widow", ContentType.movie, "2021-07-09", 134),
    ("Black Panther", ContentType.movie, "2018-02-16", 134),
    ("Spider-Man: Homecoming", ContentType.movie, "2017-07-07", 133),
    ("The Punisher – Temporada 1", ContentType.series, "2017-11-17", 676),
    ("Doctor Strange", ContentType.movie, "2016-11-04", 115),
    ("Agents of S.H.I.E.L.D. – Temporada 4", ContentType.series, "2016-09-20", 990),
    ("Iron Fist – Temporada 1", ContentType.series, "2017-03-17", 676),
    ("The Defenders", ContentType.series, "2017-08-18", 440),
    # Era 9 — Ragnarok e o Fim da Saga do Infinito
    ("The Punisher – Temporada 2", ContentType.series, "2019-01-18", 676),
    ("Jessica Jones – Temporada 2", ContentType.series, "2018-03-08", 676),
    ("Luke Cage – Temporada 2", ContentType.series, "2018-06-22", 676),
    ("Iron Fist – Temporada 2", ContentType.series, "2018-09-07", 440),
    ("Daredevil – Temporada 3", ContentType.series, "2018-10-19", 676),
    ("Thor: Ragnarok", ContentType.movie, "2017-11-03", 130),
    ("Agents of S.H.I.E.L.D. – Temporada 5", ContentType.series, "2017-12-01", 990),
    ("Ant-Man and the Wasp", ContentType.movie, "2018-07-06", 118),
    ("Avengers: Infinity War", ContentType.movie, "2018-04-27", 149),
    # Era 10 — O Blip e o Retorno
    ("Agents of S.H.I.E.L.D. – Temporada 6", ContentType.series, "2019-05-10", 594),
    ("Agents of S.H.I.E.L.D. – Temporada 7", ContentType.series, "2020-05-27", 594),
    ("Avengers: Endgame", ContentType.movie, "2019-04-26", 181),
    # Era 11 — Saga do Multiverso
    ("Loki – Temporada 1", ContentType.series, "2021-06-09", 360),
    ("What If...? – Temporada 1", ContentType.series, "2021-08-11", 360),
    ("WandaVision", ContentType.series, "2021-01-15", 396),
    ("The Falcon and the Winter Soldier", ContentType.series, "2021-03-19", 360),
    ("Shang-Chi and the Legend of the Ten Rings", ContentType.movie, "2021-09-03", 132),
    ("Eternals", ContentType.movie, "2021-11-05", 156),
    ("Spider-Man: Far From Home", ContentType.movie, "2019-07-02", 129),
    ("Spider-Man: No Way Home", ContentType.movie, "2021-12-17", 148),
    ("Hawkeye", ContentType.series, "2021-11-24", 360),
    ("Doctor Strange in the Multiverse of Madness", ContentType.movie, "2022-05-06", 126),
    ("Moon Knight", ContentType.series, "2022-03-30", 360),
    ("Ms. Marvel", ContentType.series, "2022-06-08", 360),
    ("She-Hulk: Attorney at Law", ContentType.series, "2022-08-18", 360),
    ("Thor: Love and Thunder", ContentType.movie, "2022-07-08", 119),
    ("Werewolf by Night", ContentType.special, "2022-10-07", 52),
    ("Black Panther: Wakanda Forever", ContentType.movie, "2022-11-11", 161),
    ("The Guardians of the Galaxy Holiday Special", ContentType.special, "2022-11-25", 44),
    ("Ant-Man and the Wasp: Quantumania", ContentType.movie, "2023-02-17", 125),
    ("Guardians of the Galaxy Vol. 3", ContentType.movie, "2023-05-05", 150),
    ("Secret Invasion", ContentType.series, "2023-06-21", 360),
    ("The Marvels", ContentType.movie, "2023-11-10", 105),
    ("Loki – Temporada 2", ContentType.series, "2023-10-05", 360),
    ("Echo", ContentType.series, "2024-01-09", 300),
    ("Deadpool & Wolverine", ContentType.movie, "2024-07-26", 128),
    ("Agatha All Along", ContentType.series, "2024-09-18", 540),
    ("Ironheart", ContentType.series, "2025-06-24", 360),
    ("Daredevil: Born Again", ContentType.series, "2025-03-04", 540),
    ("Captain America: Brave New World", ContentType.movie, "2025-02-14", 118),
    ("Thunderbolts*", ContentType.movie, "2025-05-02", 127),
    ("The Fantastic Four: First Steps", ContentType.movie, "2025-07-25", 130),
    ("Avengers: Doomsday", ContentType.movie, "2026-05-01", 150),
    # Era 12 — opcional
    ("X-Men '97", ContentType.series, "2024-03-20", 660),
    ("Marvel Zombies", ContentType.series, "2025-10-03", 360),
    ("Your Friendly Neighborhood Spider-Man", ContentType.series, "2025-01-29", 360),
    ("Spider-Man – Trilogia (Sam Raimi)", ContentType.series, None, 390),
    ("The Amazing Spider-Man – Duologia", ContentType.series, None, 260),
    ("X-Men – Franquia", ContentType.series, None, 990),
]

MARATHON_ITEMS: list[tuple[str, str, int, bool]] = [
    # Era 1
    ("Captain America: The First Avenger", "Era da Segunda Guerra e Pós-Guerra", 1, True),
    ("Agent Carter", "Era da Segunda Guerra e Pós-Guerra", 2, True),
    ("Agent Carter – Temporada 1", "Era da Segunda Guerra e Pós-Guerra", 3, True),
    ("Agent Carter – Temporada 2", "Era da Segunda Guerra e Pós-Guerra", 4, True),
    # Era 2
    ("Captain Marvel", "Década de 1990", 5, True),
    # Era 3
    ("Iron Man", "Início da Era dos Heróis", 6, True),
    ("Iron Man 2", "Início da Era dos Heróis", 7, True),
    ("The Incredible Hulk", "Início da Era dos Heróis", 8, True),
    ("The Consultant", "Início da Era dos Heróis", 9, True),
    ("A Funny Thing Happened on the Way to Thor's Hammer", "Início da Era dos Heróis", 10, True),
    ("Thor", "Início da Era dos Heróis", 11, True),
    ("The Avengers", "Início da Era dos Heróis", 12, True),
    ("Item 47", "Início da Era dos Heróis", 13, True),
    # Era 4
    ("Iron Man 3", "Pós-Batalha de Nova York", 14, True),
    ("All Hail the King", "Pós-Batalha de Nova York", 15, True),
    ("Agents of S.H.I.E.L.D. – Temporada 1", "Pós-Batalha de Nova York", 16, True),
    ("Thor: The Dark World", "Pós-Batalha de Nova York", 17, True),
    ("Captain America: The Winter Soldier", "Pós-Batalha de Nova York", 18, True),
    ("Agents of S.H.I.E.L.D. – Temporada 2", "Pós-Batalha de Nova York", 19, True),
    # Era 5
    ("Guardians of the Galaxy", "Expansão Cósmica", 20, True),
    ("Guardians of the Galaxy Vol. 2", "Expansão Cósmica", 21, True),
    # Era 6
    ("Daredevil – Temporada 1", "Ascensão dos Vigilantes de Rua", 22, True),
    ("Jessica Jones – Temporada 1", "Ascensão dos Vigilantes de Rua", 23, True),
    # Era 7
    ("Avengers: Age of Ultron", "Era de Ultron", 24, True),
    ("Ant-Man", "Era de Ultron", 25, True),
    ("Daredevil – Temporada 2", "Era de Ultron", 26, True),
    ("Luke Cage – Temporada 1", "Era de Ultron", 27, True),
    ("Agents of S.H.I.E.L.D. – Temporada 3", "Era de Ultron", 28, True),
    # Era 8
    ("Captain America: Civil War", "Guerra Civil", 29, True),
    ("Black Widow", "Guerra Civil", 30, True),
    ("Black Panther", "Guerra Civil", 31, True),
    ("Spider-Man: Homecoming", "Guerra Civil", 32, True),
    ("The Punisher – Temporada 1", "Guerra Civil", 33, True),
    ("Doctor Strange", "Guerra Civil", 34, True),
    ("Agents of S.H.I.E.L.D. – Temporada 4", "Guerra Civil", 35, True),
    ("Iron Fist – Temporada 1", "Guerra Civil", 36, True),
    ("The Defenders", "Guerra Civil", 37, True),
    # Era 9
    ("The Punisher – Temporada 2", "Ragnarok e o Fim da Saga do Infinito", 38, True),
    ("Jessica Jones – Temporada 2", "Ragnarok e o Fim da Saga do Infinito", 39, True),
    ("Luke Cage – Temporada 2", "Ragnarok e o Fim da Saga do Infinito", 40, True),
    ("Iron Fist – Temporada 2", "Ragnarok e o Fim da Saga do Infinito", 41, True),
    ("Daredevil – Temporada 3", "Ragnarok e o Fim da Saga do Infinito", 42, True),
    ("Thor: Ragnarok", "Ragnarok e o Fim da Saga do Infinito", 43, True),
    ("Agents of S.H.I.E.L.D. – Temporada 5", "Ragnarok e o Fim da Saga do Infinito", 44, True),
    ("Ant-Man and the Wasp", "Ragnarok e o Fim da Saga do Infinito", 45, True),
    ("Avengers: Infinity War", "Ragnarok e o Fim da Saga do Infinito", 46, True),
    # Era 10
    ("Agents of S.H.I.E.L.D. – Temporada 6", "O Blip e o Retorno", 47, True),
    ("Agents of S.H.I.E.L.D. – Temporada 7", "O Blip e o Retorno", 48, True),
    ("Avengers: Endgame", "O Blip e o Retorno", 49, True),
    # Era 11
    ("Loki – Temporada 1", "Saga do Multiverso", 50, True),
    ("What If...? – Temporada 1", "Saga do Multiverso", 51, True),
    ("WandaVision", "Saga do Multiverso", 52, True),
    ("The Falcon and the Winter Soldier", "Saga do Multiverso", 53, True),
    ("Shang-Chi and the Legend of the Ten Rings", "Saga do Multiverso", 54, True),
    ("Eternals", "Saga do Multiverso", 55, True),
    ("Spider-Man: Far From Home", "Saga do Multiverso", 56, True),
    ("Spider-Man: No Way Home", "Saga do Multiverso", 57, True),
    ("Hawkeye", "Saga do Multiverso", 58, True),
    ("Doctor Strange in the Multiverse of Madness", "Saga do Multiverso", 59, True),
    ("Moon Knight", "Saga do Multiverso", 60, True),
    ("Ms. Marvel", "Saga do Multiverso", 61, True),
    ("She-Hulk: Attorney at Law", "Saga do Multiverso", 62, True),
    ("Thor: Love and Thunder", "Saga do Multiverso", 63, True),
    ("Werewolf by Night", "Saga do Multiverso", 64, True),
    ("Black Panther: Wakanda Forever", "Saga do Multiverso", 65, True),
    ("The Guardians of the Galaxy Holiday Special", "Saga do Multiverso", 66, True),
    ("Ant-Man and the Wasp: Quantumania", "Saga do Multiverso", 67, True),
    ("Guardians of the Galaxy Vol. 3", "Saga do Multiverso", 68, True),
    ("Secret Invasion", "Saga do Multiverso", 69, True),
    ("The Marvels", "Saga do Multiverso", 70, True),
    ("Loki – Temporada 2", "Saga do Multiverso", 71, True),
    ("Echo", "Saga do Multiverso", 72, True),
    ("Deadpool & Wolverine", "Saga do Multiverso", 73, True),
    ("Agatha All Along", "Saga do Multiverso", 74, True),
    ("Ironheart", "Saga do Multiverso", 75, True),
    ("Daredevil: Born Again", "Saga do Multiverso", 76, True),
    ("Captain America: Brave New World", "Saga do Multiverso", 77, True),
    ("Thunderbolts*", "Saga do Multiverso", 78, True),
    ("The Fantastic Four: First Steps", "Saga do Multiverso", 79, True),
    ("Avengers: Doomsday", "Saga do Multiverso", 80, True),
    # Era 12 — opcional
    ("X-Men '97", "Multiverso / Realidades Paralelas (opcional)", 81, False),
    ("Marvel Zombies", "Multiverso / Realidades Paralelas (opcional)", 82, False),
    ("Your Friendly Neighborhood Spider-Man", "Multiverso / Realidades Paralelas (opcional)", 83, False),
    ("Spider-Man – Trilogia (Sam Raimi)", "Multiverso / Realidades Paralelas (opcional)", 84, False),
    ("The Amazing Spider-Man – Duologia", "Multiverso / Realidades Paralelas (opcional)", 85, False),
    ("X-Men – Franquia", "Multiverso / Realidades Paralelas (opcional)", 86, False),
]

# ---------------------------------------------------------------------------
# Episode counts per series  (title → episode_count)
# runtime per episode = season.runtime // episode_count  (integer division)
# ---------------------------------------------------------------------------
SERIES_EPISODES: dict[str, int] = {
    # Agent Carter
    "Agent Carter – Temporada 1": 8,
    "Agent Carter – Temporada 2": 10,
    # Agents of S.H.I.E.L.D.
    "Agents of S.H.I.E.L.D. – Temporada 1": 22,
    "Agents of S.H.I.E.L.D. – Temporada 2": 21,
    "Agents of S.H.I.E.L.D. – Temporada 3": 21,
    "Agents of S.H.I.E.L.D. – Temporada 4": 22,
    "Agents of S.H.I.E.L.D. – Temporada 5": 22,
    "Agents of S.H.I.E.L.D. – Temporada 6": 12,
    "Agents of S.H.I.E.L.D. – Temporada 7": 13,
    # Netflix — Vigilantes de Rua
    "Daredevil – Temporada 1": 13,
    "Daredevil – Temporada 2": 13,
    "Daredevil – Temporada 3": 13,
    "Jessica Jones – Temporada 1": 13,
    "Jessica Jones – Temporada 2": 13,
    "Luke Cage – Temporada 1": 13,
    "Luke Cage – Temporada 2": 13,
    "Iron Fist – Temporada 1": 13,
    "Iron Fist – Temporada 2": 10,
    "The Punisher – Temporada 1": 13,
    "The Punisher – Temporada 2": 13,
    "The Defenders": 8,
    # Loki
    "Loki – Temporada 1": 6,
    "Loki – Temporada 2": 6,
    # What If...?
    "What If...? – Temporada 1": 9,
    # Disney+ series
    "WandaVision": 9,
    "The Falcon and the Winter Soldier": 6,
    "Hawkeye": 6,
    "Moon Knight": 6,
    "Ms. Marvel": 6,
    "She-Hulk: Attorney at Law": 9,
    "Secret Invasion": 6,
    "Echo": 5,
    "Agatha All Along": 9,
    "Ironheart": 6,
    "Daredevil: Born Again": 9,
}


# ---------------------------------------------------------------------------
# Seed logic
# ---------------------------------------------------------------------------

def seed(db: Session) -> None:
    # Guard: skip if already seeded
    if db.query(Universe).filter(Universe.slug == "mcu").first():
        print("Seed already applied, skipping.")
        return

    print("Seeding universe...")
    universe = Universe(**UNIVERSE)
    db.add(universe)
    db.flush()

    print("Seeding marathon...")
    marathon = Marathon(universe_id=universe.id, **MARATHON)
    db.add(marathon)
    db.flush()

    print("Seeding eras...")
    era_map: dict[str, Era] = {}
    for name, position in ERAS:
        era = Era(marathon_id=marathon.id, name=name, position=position)
        db.add(era)
        db.flush()
        era_map[name] = era

    print("Seeding contents...")
    content_map: dict[str, Content] = {}
    for title, ctype, release_date, runtime in CONTENTS:
        content = Content(
            title=title,
            type=ctype,
            release_date=release_date,
            runtime=runtime,
        )
        db.add(content)
        db.flush()
        content_map[title] = content

    print("Seeding episodes...")
    episode_count = 0
    for series_title, num_episodes in SERIES_EPISODES.items():
        parent = content_map.get(series_title)
        if not parent:
            print(f"  WARNING: series not found in content_map: {series_title}")
            continue
        ep_runtime = (parent.runtime or 0) // num_episodes
        for ep_num in range(1, num_episodes + 1):
            ep = Content(
                title=f"Ep {ep_num}",
                type=ContentType.episode,
                release_date=parent.release_date,
                runtime=ep_runtime,
                episode_number=ep_num,
                parent_id=parent.id,
            )
            db.add(ep)
        episode_count += num_episodes
    db.flush()

    print("Seeding marathon items...")
    for title, era_name, position, canonical in MARATHON_ITEMS:
        item = MarathonItem(
            marathon_id=marathon.id,
            content_id=content_map[title].id,
            era_id=era_map[era_name].id,
            position=position,
            canonical=canonical,
        )
        db.add(item)

    db.commit()
    print(
        f"Done! {len(CONTENTS)} contents, {episode_count} episodes, "
        f"{len(MARATHON_ITEMS)} items, {len(ERAS)} eras."
    )


def seed_episodes(db: Session) -> None:
    """Idempotent: create episode rows for any series that doesn't have them yet.

    Safe to run on an already-seeded database -- skips series that already
    have at least one child Content(type=episode).
    """
    inserted = 0
    for series_title, num_episodes in SERIES_EPISODES.items():
        parent = (
            db.query(Content)
            .filter(Content.title == series_title, Content.type == ContentType.series)
            .first()
        )
        if not parent:
            print(f"  seed_episodes: series not found, skipping -- {series_title!r}")
            continue

        already = (
            db.query(Content)
            .filter(Content.parent_id == parent.id)
            .count()
        )
        if already > 0:
            continue  # already seeded, skip

        ep_runtime = (parent.runtime or 0) // num_episodes
        for ep_num in range(1, num_episodes + 1):
            ep = Content(
                title=f"Ep {ep_num}",
                type=ContentType.episode,
                release_date=parent.release_date,
                runtime=ep_runtime,
                episode_number=ep_num,
                parent_id=parent.id,
            )
            db.add(ep)
        inserted += num_episodes

    db.commit()
    if inserted:
        print(f"seed_episodes: inserted {inserted} episode rows.")
    else:
        print("seed_episodes: all series already have episodes, nothing to do.")


def seed_canonical_flags(db: Session) -> None:
    """Idempotent: update canonical flag for Netflix series that were previously False."""
    netflix_series = [
        "Daredevil – Temporada 1",
        "Daredevil – Temporada 2",
        "Daredevil – Temporada 3",
        "Jessica Jones – Temporada 1",
        "Jessica Jones – Temporada 2",
        "Luke Cage – Temporada 1",
        "Luke Cage – Temporada 2",
        "Iron Fist – Temporada 1",
        "Iron Fist – Temporada 2",
        "The Punisher – Temporada 1",
        "The Punisher – Temporada 2",
        "The Defenders",
    ]
    updated = (
        db.query(MarathonItem)
        .join(MarathonItem.content)
        .filter(Content.title.in_(netflix_series))
        .filter(MarathonItem.canonical.is_(False))
        .all()
    )
    for item in updated:
        item.canonical = True
    db.commit()
    if updated:
        print(f"seed_canonical_flags: updated {len(updated)} items to canonical=True.")
    else:
        print("seed_canonical_flags: nothing to update.")


def seed_remove_items(db: Session) -> None:
    """Idempotent: remove marathon items and content for dropped series."""
    removed_titles = ["Inhumans", "Runaways", "Cloak & Dagger"]
    for title in removed_titles:
        content = (
            db.query(Content)
            .filter(Content.title == title)
            .first()
        )
        if not content:
            continue
        # Remove marathon items first (FK constraint)
        db.query(MarathonItem).filter(MarathonItem.content_id == content.id).delete()
        db.delete(content)
        print(f"seed_remove_items: removed {title!r}.")
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        seed(db)              # no-op if universe already exists
        seed_episodes(db)     # idempotent: fills in missing episodes
        seed_canonical_flags(db)  # idempotent: fix Netflix series canonical flag
        seed_remove_items(db)     # idempotent: remove dropped series
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()