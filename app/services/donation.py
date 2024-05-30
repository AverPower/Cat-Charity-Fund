def donate_calculation(
    left_money: int,
    sources: list[tuple[int, int]]
):
    update_sources = []
    for source in sources:
        donation = min(left_money, source[0] - source[1])
        left_money -= donation
        update_sources.append((source[0], source[1] + donation))
        if not left_money:
            break
    return left_money, update_sources
