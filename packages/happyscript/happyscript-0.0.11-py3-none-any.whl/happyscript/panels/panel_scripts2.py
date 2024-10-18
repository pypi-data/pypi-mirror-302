import wx
from .panelsbase import PanelScripts_Base
class PanelScripts2( PanelScripts_Base):
    def __init__( self, parent, script_reader, script_control ):
        PanelScripts_Base.__init__(self, parent)
        self._reader = script_reader
        self._script_ctrl = script_control
        self.tree_root = self.treeScripts.AddRoot("DUMMY")
        self.load_treeview()
    def load_treeview(self):
        tree = self.treeScripts
        expanded_files = list()
        (child, cookie) = tree.GetFirstChild(self.tree_root)
        while child.IsOk():
            if tree.IsExpanded(child):
                expanded_files.append(tree.GetItemText(child))
            (child, cookie) = tree.GetNextChild(self.tree_root, cookie)
        tree.DeleteChildren(self.tree_root)
        for modname in self._reader.get_file_list():
            child = tree.AppendItem(self.tree_root, modname)
            for funcname in self._reader.get_func_names(modname):
                tree.AppendItem(child, funcname)
            if modname in expanded_files:
                tree.Expand(child)
    def OnBtnReload( self, event ):
        if self._script_ctrl.is_busy():
            msg = "A script is still running.  Press 'abort' first."
            wx.MessageBox( msg, "HappyScript", wx.OK | wx.ICON_WARNING )
            return
        self._reader.reload()
        self.load_treeview()
    def OnTreeLeftDoubleClick( self, event ):
        pt = event.GetPosition();
        item, _ = self.treeScripts.HitTest(pt)
        self.ExecuteScriptForItem(item)
    def OnTreeKeyDown( self, event ):
        keycode = event.GetKeyCode()
        if keycode==wx.WXK_RETURN:
            item = self.treeScripts.GetSelection()
            self.ExecuteScriptForItem(item)
    def ExecuteScriptForItem(self, item):
        if item:
            parent = self.treeScripts.GetItemParent(item)
            if parent.IsOk() and parent!=self.tree_root:
                if self._script_ctrl.is_busy():
                    print("Another script is already running")
                else:
                    filename = self.treeScripts.GetItemText(parent)
                    funcname = self.treeScripts.GetItemText(item)
                    scriptname = "%s.%s.%s" % (self._reader.group_name, filename, funcname)
                    self._script_ctrl.run(scriptname)
    def OnTreeSelChanged( self, event ):
        txt = "no help"
        try:
            item = event.GetItem()
            if item:
                parent = self.treeScripts.GetItemParent(item)
                if parent.IsOk() and parent!=self.tree_root:
                    filename = self.treeScripts.GetItemText(parent)
                    funcname = self.treeScripts.GetItemText(item)
                    txt = self._reader.get_help(filename, funcname)
        except:
            pass
        self.txtHelp.SetValue(txt)
        event.Skip()
    def btn_stopOnButtonClick( self, event ):
        self._script_ctrl.stop()
