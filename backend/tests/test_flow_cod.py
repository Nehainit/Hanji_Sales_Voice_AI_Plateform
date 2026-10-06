from app.voice.flow_cod import FLOW, SCRIPT, render, validate


def test_flow_is_valid():
    assert validate() == []


def test_every_branch_reaches_an_outcome():
    def ends(node, seen=()):
        n = FLOW[node]
        if "end" in n:
            return True
        return all(t not in seen and ends(t, seen + (node,)) for t in n["next"].values())

    assert ends("greet")


def test_render_fills_order_values():
    text = render(SCRIPT["greet"], {"name": "Priya", "brand": "Kesar Kurtis", "agent": "Ananya",
                                    "amount": "₹1,299", "product": "Anarkali Kurti"})
    assert "Priya ji" in text and "₹1,299" in text and "{" not in text


def test_render_male_agent_switches_verbs():
    assert "raha hoon" in render(SCRIPT["greet"], {}, agent_is_male=True)


def test_render_keeps_unknown_placeholders():
    assert "{address}" in render(SCRIPT["confirm_address"], {})
