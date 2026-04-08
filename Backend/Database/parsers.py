import re


def clean_html(raw_text: str) -> str:
    if not raw_text:
        return ""
    return re.sub(r'<[^>]+>', '', raw_text)


def parse_tooltip(tooltip: str, effect_burn: list, vars_list: list) -> str:
    """
    Translates Riots variable ({{ eN}}, {{aN}}) based on the official docs.
    :param tooltip:
    :param effect_burn:
    :param vars_list:
    :return:
    """

    if not tooltip: return ""

    def replace_e(match):
        index = int(match.group(1))
        if effect_burn and index < len(effect_burn) and effect_burn[index] is not None:
            return str(effect_burn[index])
        return "??" # fallback if riot doesn't provide data

    tooltip = re.sub(r'\{\{\s*e(\d+)\s*\}\}', replace_e, tooltip)

    def replace_vars(match):
        var_key = match.group(1)
        if vars_list:
            for v in vars_list:
                if v.get("key") == var_key:
                    coeffs = v.get("coeff", [])
                    if coeffs:
                        # Sometimes the coefficient is a single number, sometimes an array. We simplify it to a string.
                        return "/".join(str(c) for c in coeffs) if len(set(coeffs)) > 1 else str(coeffs[0])
        return "??"

    tooltip = re.sub(r'\{\{\s*([af]\d+)\s*\}\}', replace_vars, tooltip)

    tooltip = re.sub(r'\{\{\s*[^}]+\s*\}\}', '[dependent on stats]', tooltip)

    return clean_html(tooltip)


def parse_resource(resource_text: str, cost_burn: str, effect_burn: list) -> str:
    """
    Translates spell cost based on the rule 'Calculating Spell Costs' from Riot docs
    :param resource_text:
    :param cost_burn:
    :param effect_burn:
    :return:
    """
    if not resource_text or resource_text == "None":
        return "No cost"

    resource_text = re.sub(r'\{\{\s*cost\s*\}\}', str(cost_burn), resource_text)

    def replace_e(match):
        index = int(match.group(1))
        if effect_burn and index < len(effect_burn) and effect_burn[index] is not None:
            return str(effect_burn[index])
        return "??"

    resource_text = re.sub(r'\{\{\s*e(\d+)\s*\}\}', replace_e, resource_text)

    return clean_html(resource_text)


def clean_item_description(raw_text: str) -> str:
    """Clears the item description of Riot's HTML tags, preserving readability."""
    if not raw_text:
        return ""
    text = re.sub(r'<br\s*/?>', ' ', raw_text)
    text = re.sub(r'<li>', ' * ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def prepare_item_for_vectorization(item_data, clean_desc: str) -> str:
    name = item_data.get("name", "")
    tags = ", ".join(item_data.get("tags", []))
    plaintext = item_data.get("plaintext", "")

    vector_text = f"Item Name: {name}. "
    if tags: vector_text += f"Tags: {tags}. "
    if plaintext: vector_text += f"Summary: {plaintext} "
    if clean_desc: vector_text += f"Description: {clean_desc}"

    return vector_text.strip()
