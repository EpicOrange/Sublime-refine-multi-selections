import itertools
from functools import reduce
import sublime, sublime_plugin

def pairwise_norepeat(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))[0::2]

def selection_positions(selections):
    positions = set()
    for i in selections:
        positions.add(i.a)
        positions.add(i.b)
    return sorted(positions)

# default: cmd-k cmd-s
class SelectSelectionEdgesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel()
        positions = selection_positions(selections)
        new_selections = map(lambda x: sublime.Region(x, x), positions)
        selections.clear()
        selections.add_all(new_selections)

# default: cmd-k cmd-shift-s
class UndoSelectSelectionEdgesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel()
        positions = selection_positions(selections)
        paired_positions = pairwise_norepeat(positions)
        new_selections = map(lambda p: sublime.Region(p[0], p[1]), paired_positions)
        selections.clear()
        selections.add_all(new_selections)

def flip_selection(self, region):
    self.view.sel().subtract(region)
    self.view.sel().add(sublime.Region(region.b, region.a))

# default: cmd-k cmd-f
class FlipSelectionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            flip_selection(self, region)

# default: cmd-k cmd-e
class OrientSelectionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.a > region.b:
                flip_selection(self, region)

# default: cmd-alt-delete
# todo: pressing again retains every third selection instead (making use of soft undo)
class DeleteEveryOtherSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("hi")
        for region in sorted(self.view.sel())[1::2]:
            self.view.sel().subtract(region)

# Intended as replacement for self.view.sel().subtract(region)
# https://sublimetext.userecho.com/communities/1/topics/4315-subtract-select-not-working-properly-api
def region_difference(regionA, regionB):
    intersect = regionA.intersection(regionB)
    if intersect.size() == 0:
        return [regionA]
    else:
        return [sublime.Region(regionA.a, intersect.a),
                sublime.Region(intersect.b, regionA.b)]

def region_difference_all(region, regions):
    result = [region]
    for to_remove in regions:
        result = [x for r in result
                    for x in region_difference(r, to_remove)
                    if x.size() > 0]
    return result

# default: cmd-i
class InvertSelectionInLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel()
        selections_list = list(self.view.sel())
        covered_lines = self.view.line(reduce(lambda x, y: x.cover(y), selections_list))
        result = region_difference_all(covered_lines, selections)
        selections.clear()
        selections.add_all(result)
