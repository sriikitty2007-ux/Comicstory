def build_comic_layout(
    outline: list[dict],
    story: list[dict],
    image_paths: list[str],
) -> list[dict]:

    story_by_number = {
        item["panel_number"]: item
        for item in story
    }

    layout = []

    for index, panel in enumerate(outline):

        narrative = story_by_number.get(
            panel["panel_number"],
            {},
        )

        layout.append(
            {
                "panel_number": panel["panel_number"],
                "title": narrative.get(
                    "title",
                    panel["title"],
                ),
                "scene_description": panel[
                    "scene_description"
                ],
                "image_prompt": panel[
                    "image_prompt"
                ],
                "image_path": image_paths[index],
                "caption": narrative.get(
                    "caption",
                    "",
                ),
                "narration": narrative.get(
                    "narration",
                    "",
                ),
                "dialogue": narrative.get(
                    "dialogue",
                    "",
                ),
            }
        )

    return layout