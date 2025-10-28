from insight_bot.gestaltview_plk import GestaltViewPLK

def test_plk_analysis():
    plk = GestaltViewPLK()
    result = plk.analyze("This is a test sentence.")
    assert "resonance_score" in result
    assert isinstance(result["resonance_score"], int)