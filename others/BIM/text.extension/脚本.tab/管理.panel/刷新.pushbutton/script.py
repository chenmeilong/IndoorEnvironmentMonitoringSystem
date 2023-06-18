
import xlrd
from pyrevit import HOST_APP
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms


my_config = script.get_config()


def setup_style_per_config(from_style, to_style):
    # base
    if my_config.get_option('halftone', True):
        to_style.SetHalftone(from_style.Halftone)

    if my_config.get_option('transparency', True):
        to_style.SetSurfaceTransparency(from_style.Transparency)

    # projections
    if my_config.get_option('proj_line_color', True):
        to_style.SetProjectionLineColor(from_style.ProjectionLineColor)
    if my_config.get_option('proj_line_pattern', True):
        to_style.SetProjectionLinePatternId(from_style.ProjectionLinePatternId)
    if my_config.get_option('proj_line_weight', True):
        to_style.SetProjectionLineWeight(from_style.ProjectionLineWeight)

    if HOST_APP.is_newer_than(2019, or_equal=True):
        if my_config.get_option('proj_fill_color', True):
            to_style.SetSurfaceForegroundPatternColor(
                from_style.SurfaceForegroundPatternColor
                )
        if my_config.get_option('proj_fill_pattern', True):
            to_style.SetSurfaceForegroundPatternId(
                from_style.SurfaceForegroundPatternId
                )
        if my_config.get_option('proj_fill_pattern_visibility', True):
            to_style.SetSurfaceForegroundPatternVisible(
                from_style.IsSurfaceForegroundPatternVisible
                )
        if my_config.get_option('proj_bg_fill_color', True):
            to_style.SetSurfaceBackgroundPatternColor(
                from_style.SurfaceBackgroundPatternColor
                )
        if my_config.get_option('proj_bg_fill_pattern', True):
            to_style.SetSurfaceBackgroundPatternId(
                from_style.SurfaceBackgroundPatternId
                )
        if my_config.get_option('proj_bg_fill_pattern_visibility', True):
            to_style.SetSurfaceBackgroundPatternVisible(
                from_style.IsSurfaceBackgroundPatternVisible
                )
    else:
        if my_config.get_option('proj_fill_color', True):
            to_style.SetProjectionFillColor(
                from_style.ProjectionFillColor
                )
        if my_config.get_option('proj_fill_pattern', True):
            to_style.SetProjectionFillPatternId(
                from_style.ProjectionFillPatternId
                )
        if my_config.get_option('proj_fill_pattern_visibility', True):
            to_style.SetProjectionFillPatternVisible(
                from_style.IsProjectionFillPatternVisible
                )

    # cuts
    if my_config.get_option('cut_line_color', True):
        to_style.SetCutLineColor(from_style.CutLineColor)
    if my_config.get_option('cut_line_pattern', True):
        to_style.SetCutLinePatternId(from_style.CutLinePatternId)
    if my_config.get_option('cut_line_weight', True):
        to_style.SetCutLineWeight(from_style.CutLineWeight)

    if HOST_APP.is_newer_than(2019, or_equal=True):
        if my_config.get_option('cut_fill_color', True):
            to_style.SetCutForegroundPatternColor(
                from_style.CutForegroundPatternColor
                )
        if my_config.get_option('cut_fill_pattern', True):
            to_style.SetCutForegroundPatternId(
                from_style.CutForegroundPatternId
                )
        if my_config.get_option('cut_fill_pattern_visibility', True):
            to_style.SetCutForegroundPatternVisible(
                from_style.IsCutForegroundPatternVisible
                )
        if my_config.get_option('cut_bg_fill_color', True):
            to_style.SetCutBackgroundPatternColor(
                from_style.CutBackgroundPatternColor
                )
        if my_config.get_option('cut_bg_fill_pattern', True):
            to_style.SetCutBackgroundPatternId(
                from_style.CutBackgroundPatternId
                )
        if my_config.get_option('cut_bg_fill_pattern_visibility', True):
            to_style.SetCutBackgroundPatternVisible(
                from_style.IsCutBackgroundPatternVisible
                )
    else:
        if my_config.get_option('cut_fill_color', True):
            to_style.SetCutFillColor(
                from_style.CutFillColor
                )
        if my_config.get_option('cut_fill_pattern', True):
            to_style.SetCutFillPatternId(
                from_style.CutFillPatternId
                )
        if my_config.get_option('cut_fill_pattern_visibility', True):
            to_style.SetCutFillPatternVisible(
                from_style.IsCutFillPatternVisible
                )


def get_source_style(element_id):
    # get style of selected element
    from_style = revit.doc.ActiveView.GetElementOverrides(element_id)
    # make a new clean element style
    src_style = DB.OverrideGraphicSettings()
    # setup a new style per config and borrow from the selected element's style
    setup_style_per_config(from_style, src_style)
    return src_style


with forms.WarningBar(title='Pick outdoorRED object:'):                 
    source_RED_element = revit.pick_element()
with forms.WarningBar(title='Pick outdoorORANGE object:'):              
    source_ORANGE_element = revit.pick_element()
with forms.WarningBar(title='Pick outdoorYELLOW object:'):              
    source_YELLOW_element = revit.pick_element()	
with forms.WarningBar(title='Pick outdoorGREEN object:'):              
    source_GREEN_element = revit.pick_element()	

source_RED_style  =   get_source_style(source_RED_element.Id)
source_ORANGE_style = get_source_style(source_ORANGE_element.Id)
source_YELLOW_style = get_source_style(source_YELLOW_element.Id)
source_GREEN_style =  get_source_style(source_GREEN_element.Id)

with forms.WarningBar(title='Pick match indoorRED objects'):
	dest_element1 = revit.pick_element()
with forms.WarningBar(title='Pick match indoorORANGE objects'):
	dest_element2 = revit.pick_element()
with forms.WarningBar(title='Pick match indoorYELLOW objects'):
	dest_element3 = revit.pick_element()
with forms.WarningBar(title='Pick match indoorGREEN objects'):
	dest_element4 = revit.pick_element()	

while True:
	dest_element = revit.pick_element()
	if not dest_element:
         break		
	data = xlrd.open_workbook(r'd:\app\REVIT2016\Revit 2016\databuff.xls')    
	table = data.sheet_by_name('Sheel1')   
	shownumbuf=[4,4,4,4,4]
	shownumbuf[1]= table.cell(0,0).value
	shownumbuf[2]= table.cell(0,1).value
	shownumbuf[3]= table.cell(0,2).value	
	shownumbuf[4]= table.cell(0,3).value	

		
	if shownumbuf[1]==1:	
		dest_element_ids = [dest_element1.Id]
		if hasattr(dest_element1, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element1.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_RED_style)
	if shownumbuf[1]==2:	
		dest_element_ids = [dest_element1.Id]
		if hasattr(dest_element1, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element1.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_ORANGE_style)		
	if shownumbuf[1]==3:	
		dest_element_ids = [dest_element1.Id]
		if hasattr(dest_element1, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element1.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_YELLOW_style)
	if shownumbuf[1]==4:	
		dest_element_ids = [dest_element1.Id]
		if hasattr(dest_element1, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element1.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_GREEN_style)

				
				
	if shownumbuf[2]==1:	
		dest_element_ids = [dest_element2.Id]
		if hasattr(dest_element2, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element2.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_RED_style)
	if shownumbuf[2]==2:	
		dest_element_ids = [dest_element2.Id]
		if hasattr(dest_element2, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element2.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_ORANGE_style)		
	if shownumbuf[2]==3:	
		dest_element_ids = [dest_element2.Id]
		if hasattr(dest_element2, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element2.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_YELLOW_style)
	if shownumbuf[2]==4:	
		dest_element_ids = [dest_element2.Id]
		if hasattr(dest_element2, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element2.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_GREEN_style)
				
				
				
	if shownumbuf[3]==1:	
		dest_element_ids = [dest_element3.Id]
		if hasattr(dest_element3, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element3.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_RED_style)
	if shownumbuf[3]==2:	
		dest_element_ids = [dest_element3.Id]
		if hasattr(dest_element3, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element3.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_ORANGE_style)		
	if shownumbuf[3]==3:	
		dest_element_ids = [dest_element3.Id]
		if hasattr(dest_element3, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element3.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_YELLOW_style)
	if shownumbuf[3]==4:	
		dest_element_ids = [dest_element3.Id]
		if hasattr(dest_element3, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element3.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_GREEN_style)
				
	if shownumbuf[4]==1:	
		dest_element_ids = [dest_element4.Id]
		if hasattr(dest_element4, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element4.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_RED_style)
	if shownumbuf[4]==2:	
		dest_element_ids = [dest_element4.Id]
		if hasattr(dest_element4, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element4.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_ORANGE_style)		
	if shownumbuf[4]==3:	
		dest_element_ids = [dest_element4.Id]
		if hasattr(dest_element4, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element4.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_YELLOW_style)
	if shownumbuf[4]==4:	
		dest_element_ids = [dest_element4.Id]
		if hasattr(dest_element4, 'GetSubComponentIds'):
			dest_element_ids.extend(dest_element4.GetSubComponentIds())
		with revit.Transaction('Match Graphics Overrides'):
			for dest_elid in dest_element_ids:
				revit.activeview.SetElementOverrides(dest_elid, source_GREEN_style)

