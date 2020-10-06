"""
tensorx tests.

Run these tests prior to every commit.

"""
import unittest
from PyQt5.QtTest import QTest, QSignalSpy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QComboBox, QPushButton
from tensorx import __main__ as main 
# from os import listdir
# from shutil import copyfile
import pickle
from collections import namedtuple
import pandas as pd
import numpy as np
import os
import csv 

class TestTensorX(unittest.TestCase):
    """
    unittest class for single-hole model.
    
    Attributes
    ----------
    None.
    
    Methods
    -------
    todo.
    
    """
    def setUp(self):
        """
        Instantiate TensorX.

        Returns
        -------
        None.

        """
        ctx = main.AppContext()
        self.app = ctx.main_window
        
        self.fp = open(
            'tests/test_output.csv', 
            'a+',
            newline='',
            )
        self.writer = csv.writer(
            self.fp,
            )
    
    def tearDown(self):
        """
        Close TensorX instance.

        Returns
        -------
        None.

        """
        self.app.close()
        self.fp.close()
    
    def open_model(self, model, model_path=None):
        """
        Open model.

        Parameters
        ----------
        model : str
            Model.
        model_path : str, optional 
            Model path. The default is None.

        Returns
        -------
        None.

        """
        assert isinstance(model, str)
        model_map = {
            'single-hole': self.app.satellitehole_model,
            'satellite-hole': self.app.satellitehole_model,
            }
        if model == 'single-hole':
            model_path = self.app.ctx.single_hole_model
        if model_path is not None:
            assert isinstance(model_path, str)
            assert os.path.exists(model_path)
            model_path = os.path.abspath(model_path)
        
        if model in model_map.keys():
            # Select Model
            self.clickObject(model_map[model], Qt.LeftButton)
            self.assertEqual(self.app.input_tab.objectName(), model)
            
            # Configure callback
            self.app.worker_signals = main.WorkerSignals()
            
            # Open StressCheck
            sc, doc, model = self.app.open_sc_model(
                self.app.worker_signals.progress,
                model_path
                )
            
            return sc, doc, model
    
    def clickObject(self, obj, btn=Qt.LeftButton, pos=None):
        """
        Click on QObject with Qt.MouseButton.

        Parameters
        ----------
        obj : QObject
            QObject or QWidget to mouse click.
        btn : Qt.MouseButton, optional
            Mouse button to use. The default is Qt.LeftButton.
        pos : QPoint, optional
            Mouse position for click. The default is None.

        Returns
        -------
        None.

        """
        self.assertTrue(obj is not None)
        if pos is None:
            pos = QPoint(obj.width()/2, obj.height()/2)
        QTest.mouseClick(obj, btn, pos=pos)
    
    def enterField(self, field, value):
        """
        Type/Enter value into field.

        Parameters
        ----------
        field : QObject
            QLineEdit, or other QWidget with clear() attribute.
        value : float or str
            Data/Value to enter into field.

        Returns
        -------
        None.

        """
        field.clear()
        QTest.keyClicks(field, str(value))
    
    def setRepairGeometry(self, d0, th, Ef, nf=False, csk_depth=0):
        """
        Set single-hole repair geometry.

        Parameters
        ----------
        d0 : float
            Hole diameter.
        th : float
            Coupon thickness.
        Ef : float
            Coupon E, Msi.
        nf : bool, optional
            Neat-fit. The default is False.
        csk_depth : float, optional
            Countersink depth. The default is 0.

        Returns
        -------
        None.

        """
        # Click Repair CheckBox
        pos = QPoint(2, self.app.input_tab.repair_check.height()/2)
        self.clickObject(self.app.input_tab.repair_check, pos=pos)
        self.assertTrue(self.app.input_tab.repair_check.isChecked())
        
        # d0
        self.enterField(self.app.input_tab.dia_repair_value, d0)
        self.assertEqual(self.app.input_tab.coupon.r_d0, d0)
        
        # th
        self.enterField(self.app.input_tab.thk_repair_value, th)
        self.assertEqual(self.app.input_tab.coupon.r_th, th)
        
        # Ef
        self.enterField(self.app.input_tab.Ef_repair_value, Ef)
        self.assertEqual(self.app.input_tab.coupon.r_Ef0, Ef*1e6)
        
        # neat fit
        if nf:
            self.clickObject(self.app.input_tab.repair_neat_check)
            self.assertTrue(self.app.input_tab.repair_neat_check.isChecked())
        
        # csk
        if csk_depth:
            self.clickObject(self.app.input_tab.repair_csk_check)
            self.assertTrue(self.app.input_tab.repair_csk_check.isChecked())
            self.enterField(self.app.input_tab.repair_csk_value, csk_depth)
            self.assertEqual(self.app.input_tab.coupon.r_csk0, csk_depth)
    
    def setPrintGeometry(self, x0, y0, d0, w, h, th, Ep, Ef, nf=False, csk_depth=0):
        """
        Set single-hole print geometry.

        Parameters
        ----------
        x0 : float
            Hole center x-coordinate.
        y0 : float
            Hole center y-coordinate.
        d0 : float
            Hole diameter.
        w : float
            Coupon width.
        h : float
            Coupon height.
        th : float
            Coupon thickness.
        Ep : float
            Coupon E, Msi.
        Ef : float
            Fastener E, Msi.
        nf : bool, optional
            DESCRIPTION. The default is False.
        csk_depth : float, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        # x0
        self.enterField(self.app.input_tab.xoff_print_value, x0)
        self.assertEqual(self.app.input_tab.coupon.x0, x0)
        
        # y0
        self.enterField(self.app.input_tab.yoff_print_value, y0)
        self.assertEqual(self.app.input_tab.coupon.y0, y0)
        
        # d0
        self.enterField(self.app.input_tab.dia_print_value, d0)
        self.assertEqual(self.app.input_tab.coupon.d0, d0)
        
        # w
        self.enterField(self.app.input_tab.width_print_value, w)
        self.assertEqual(self.app.input_tab.coupon.w, w)
        
        # h
        self.enterField(self.app.input_tab.height_print_value, h)
        self.assertEqual(self.app.input_tab.coupon.h, h)
        
        # th
        self.enterField(self.app.input_tab.thk_print_value, th)
        self.assertEqual(self.app.input_tab.coupon.th, th)
        
        # Ep
        self.enterField(self.app.input_tab.Ep_print_value, Ep)
        self.assertEqual(self.app.input_tab.coupon.Ep, Ep*1e6)
        
        # Ef 
        self.enterField(self.app.input_tab.Ef_print_value, Ef)
        self.assertEqual(self.app.input_tab.coupon.Ef0, Ef*1e6)
        
        # neat fit
        if nf:
            self.clickObject(self.app.input_tab.print_neat_check)
            self.assertTrue(self.app.input_tab.print_neat_check.isChecked())
        
        # csk
        if csk_depth:
            self.clickObject(self.app.input_tab.print_csk_check)
            self.assertTrue(self.app.input_tab.print_csk_check.isChecked())
            self.enterField(self.app.input_tab.print_csk_value, csk_depth)
            self.assertEqual(self.app.input_tab.coupon.csk0, csk_depth)
    
    def setBypassLoad(self, fx_byp=0, fy_byp=0, v_byp=0, m_top_byp=0, m_rh_byp=0):
        """
        Set bypass load.

        Parameters
        ----------
        fx_byp : float, optional
            DESCRIPTION. The default is 0.
        fy_byp : float, optional
            DESCRIPTION. The default is 0.
        v_byp : float, optional
            DESCRIPTION. The default is 0.
        m_top_byp : float, optional
            DESCRIPTION. The default is 0.
        m_rh_byp : float, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        # Click on bypass button
        self.clickObject(self.app.input_tab.byp_button)
        self.assertTrue(self.app.input_tab.byp_button.isChecked())
        
        # Fx
        self.enterField(self.app.input_tab.value_00, fx_byp)
        # Fy
        self.enterField(self.app.input_tab.value_10, fy_byp)
        # Shear
        self.enterField(self.app.input_tab.value_20, v_byp)
        # M-top
        self.enterField(self.app.input_tab.value_01, m_top_byp)
        # M-right
        self.enterField(self.app.input_tab.value_11, m_rh_byp)
    
    def setAxialShearLoad(self, v_bot_neg=0, v_top_neg=0, v_lh_neg=0, v_rh_neg=0, v_bot_pos=0, v_top_pos=0, v_lh_pos=0, v_rh_pos=0):
        """
        Set axial-shear load.

        Parameters
        ----------
        v_bot_neg : float, optional
            DESCRIPTION. The default is 0.
        v_top_neg : float, optional
            DESCRIPTION. The default is 0.
        v_lh_neg : float, optional
            DESCRIPTION. The default is 0.
        v_rh_neg : float, optional
            DESCRIPTION. The default is 0.
        v_bot_pos : float, optional
            DESCRIPTION. The default is 0.
        v_top_pos : float, optional
            DESCRIPTION. The default is 0.
        v_lh_pos : float, optional
            DESCRIPTION. The default is 0.
        v_rh_pos : float, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        # Click on axial-shear button
        self.clickObject(self.app.input_tab.axial_shear_button)
        self.assertTrue(self.app.input_tab.axial_shear_button.isChecked())
        
        # V-bottom-negative
        self.enterField(self.app.input_tab.value_00, v_bot_neg)
        # V-top-negative
        self.enterField(self.app.input_tab.value_10, v_top_neg)
        # V-left-negative
        self.enterField(self.app.input_tab.value_20, v_lh_neg)
        # V-right-negative
        self.enterField(self.app.input_tab.value_30, v_rh_neg)
        # V-bottom-positive
        self.enterField(self.app.input_tab.value_01, v_bot_pos)
        # V-top-positive
        self.enterField(self.app.input_tab.value_11, v_top_pos)
        # V-left-positive
        self.enterField(self.app.input_tab.value_21, v_lh_pos)
        # V-right-positive
        self.enterField(self.app.input_tab.value_31, v_rh_pos)
    
    def setBearingAxialLoad(self, px_pos=0, px_neg=0, py_pos=0, py_neg=0):
        """
        Set bearing-axial load.

        Parameters
        ----------
        px_pos : float, optional
            DESCRIPTION. The default is 0.
        px_neg : float, optional
            DESCRIPTION. The default is 0.
        py_pos : float, optional
            DESCRIPTION. The default is 0.
        py_neg : float, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        # Click Bearing-Axial Button
        self.clickObject(self.app.input_tab.brg_axial_button)
        self.assertTrue(self.app.input_tab.brg_axial_button.isChecked())
        
        # Px-positive
        self.enterField(self.app.input_tab.value_00, px_pos)
        # Px-negative 
        self.enterField(self.app.input_tab.value_10, px_neg)
        # Py-positive 
        self.enterField(self.app.input_tab.value_20, py_pos)
        # Py-negative 
        self.enterField(self.app.input_tab.value_30, py_neg)
    
    def setBearingShearLoad(self, vbs_bot_neg=0, vbs_top_neg=0, vbs_lh_neg=0, vbs_rh_neg=0):
        """
        Set bearing-shear load.

        Parameters
        ----------
        vbs_bot_neg : float, optional
            DESCRIPTION. The default is 0.
        vbs_top_neg : float, optional
            DESCRIPTION. The default is 0.
        vbs_lh_neg : float, optional
            DESCRIPTION. The default is 0.
        vbs_rh_neg : float, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        # Click Bearing-Shear Button
        self.clickObject(self.app.input_tab.brg_shear_button)
        self.assertTrue(self.app.input_tab.brg_shear_button.isChecked())
        
        # Bottom-Negative 
        self.enterField(self.app.input_tab.value_00, vbs_bot_neg)
        # Top-Negative 
        self.enterField(self.app.input_tab.value_10, vbs_top_neg)
        # Left-Negative 
        self.enterField(self.app.input_tab.value_20, vbs_lh_neg)
        # Right-Negative 
        self.enterField(self.app.input_tab.value_30, vbs_rh_neg)
    
    def verifyCouponBalance(self, px=0.0, py=0.0, fx_top_byp=0.0, fx_top_brg=0.0, fy_top_byp=0.0, fy_top_brg=0.0, m_top_byp=0.0, m_top_brg=0.0, fx_rh_byp=0.0, fx_rh_brg=0.0, fy_rh_byp=0.0, fy_rh_brg=0.0, m_rh_byp=0.0, m_rh_brg=0.0, fx_bot_byp=0.0, fx_bot_brg=0.0, fy_bot_byp=0.0, fy_bot_brg=0.0, m_bot_byp=0.0, m_bot_brg=0.0, fx_lh_byp=0.0, fx_lh_brg=0.0, fy_lh_byp=0.0, fy_lh_brg=0.0, m_lh_byp=0.0, m_lh_brg=0.0, delta=1.0):
        """
        Verify coupon force/moment balance.

        Parameters
        ----------
        px : float, optional
            Bearing x-direction. The default is 0.0.
        py : float, optional
            Bearing y-direction. The default is 0.0.
        fx_top_byp : float, optional
            Bypass top, x-direction. The default is 0.0.
        fx_top_brg : float, optional
            Bearing top, x-direction. The default is 0.0.
        fy_top_byp : float, optional
            Bypass top, y-direction. The default is 0.0.
        fy_top_brg : float, optional
            Bearing top, y-direction. The default is 0.0.
        m_top_byp : float, optional
            Bypass moment, top. The default is 0.0.
        m_top_brg : float, optional
            Bearing moment, top. The default is 0.0.
        fx_rh_byp : float, optional
            DESCRIPTION. The default is 0.0.
        fx_rh_brg : float, optional
            DESCRIPTION. The default is 0.0.
        fy_rh_byp : float, optional
            DESCRIPTION. The default is 0.0.
        fy_rh_brg : float, optional
            DESCRIPTION. The default is 0.0.
        m_rh_byp : float, optional
            DESCRIPTION. The default is 0.0.
        m_rh_brg : float, optional
            DESCRIPTION. The default is 0.0.
        fx_bot_byp : float, optional
            DESCRIPTION. The default is 0.0.
        fx_bot_brg : float, optional
            DESCRIPTION. The default is 0.0.
        fy_bot_byp : float, optional
            DESCRIPTION. The default is 0.0.
        fy_bot_brg : float, optional
            DESCRIPTION. The default is 0.0.
        m_bot_byp : float, optional
            DESCRIPTION. The default is 0.0.
        m_bot_brg : float, optional
            DESCRIPTION. The default is 0.0.
        fx_lh_byp : float, optional
            DESCRIPTION. The default is 0.0.
        fx_lh_brg : float, optional
            DESCRIPTION. The default is 0.0.
        fy_lh_byp : float, optional
            DESCRIPTION. The default is 0.0.
        fy_lh_brg : float, optional
            DESCRIPTION. The default is 0.0.
        m_lh_byp : float, optional
            DESCRIPTION. The default is 0.0.
        m_lh_brg : float, optional
            DESCRIPTION. The default is 0.0.
        delta : float, optional
            Difference in value, lb. The default is 1.0.

        Returns
        -------
        None.

        """
        # Bearing
        self.assertAlmostEqual(self.app.input_tab.coupon.Px, px, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Py, py, delta=delta)
        
        # Bypass
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_top_byp, fx_top_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_top_byp, fy_top_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_top_byp, m_top_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_rh_byp, fx_rh_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_rh_byp, fy_rh_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_rh_byp, m_rh_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_bot_byp, fx_bot_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_bot_byp, fy_bot_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_bot_byp, m_bot_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_lh_byp, fx_lh_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_lh_byp, fy_lh_byp, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_lh_byp, m_lh_byp, delta=delta)
        
        # Bearing
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_top_brg, fx_top_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_top_brg, fy_top_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_top_brg, m_top_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_rh_brg, fx_rh_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_rh_brg, fy_rh_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_rh_brg, m_rh_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_bot_brg, fx_bot_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_bot_brg, fy_bot_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_bot_brg, m_bot_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fx_lh_brg, fx_lh_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.Fy_lh_brg, fy_lh_brg, delta=delta)
        self.assertAlmostEqual(self.app.input_tab.coupon.M_lh_brg, m_lh_brg, delta=delta)
    
    def verifyCriticalResults(self, results, kts, loc, kckt, gr):
        """
        Verify critical fatigue stress quantities and solution error < 5%.

        Parameters
        ----------
        results : dict
            Dictionary of fatigue stress quantities.
        kts : float
            DESCRIPTION.
        loc : str
            DESCRIPTION.
        kckt : float
            DESCRIPTION.
        gr : float
            DESCRIPTION.

        Returns
        -------
        None.

        """
        surf, angle = results.get('location', {}).get(0, '').split(', ')
        angle = float(angle.split()[0])
        self.assertAlmostEqual(results.get('kts', {}).get(0, 0), kts, delta=1000)
        self.assertEqual(surf, loc.split(', ')[0])
        self.assertAlmostEqual(angle, float(loc.split(', ')[-1].split()[0]), delta=5)
        self.assertAlmostEqual(results.get('kckt', {}).get(0, 0), kckt, delta=0.10)
        self.assertAlmostEqual(results.get('gradient ratio', {}).get(0, 0), gr, delta=0.10)
        self.assertTrue(results.get('solution error', 100) < 5.0)
    
    def setQcomboboxIndex(self, widget, text):
        """
        Set QComboBox index to text value.

        Parameters
        ----------
        widget : QComboBox
            QComboBox widget.
        text : str
            String/item to set as current index.

        Returns
        -------
        None.

        """
        self.assertTrue(widget is not None)
        self.assertTrue(text in [widget.itemText(i) for i in range(widget.count())])
        widget.setCurrentIndex(widget.findText(text))
        self.assertEqual(widget.currentText(), text)
    
    def setPlateMaterial(self, matl_type='Aluminum', matl_subtype='7050-T74', matl_form='Plate', matl_grain='L-T', matl_stock=4.5, matl_finish='≤ 125', matl_coating='N/A', matl_condition='Annealed', repair=False):
        """
        Set plate material values.

        Parameters
        ----------
        matl_type : str, optional
            Material. The default is 'Aluminum'.
        matl_subtype : str, optional
            Material alloy and/or temper. The default is '7050-T74'.
        matl_form : str, optional
            Material form. The default is 'Plate'.
        matl_grain : str, optional
            Material grain direction. The default is 'L-T'.
        matl_stock : str, optional
            Material stock thickness. The default is 4.5".
        matl_finish : str, optional
            Material surface finish RHR/Ra. The default is '≤ 125'.
        matl_coating : str, optional
            Material surface coating. The default is 'N/A'.
        matl_condition : str, optional
            Material surface condition. The default is 'Annealed'.
        repair : str, optional
            Repair or print values. The default is False.

        Returns
        -------
        None.

        """
        if repair:
            matl_type_widget = self.app.report_tab.repair_matl_box
            matl_subtype_widget = self.app.report_tab.repair_matl_value
            matl_form_widget = self.app.report_tab.repair_form_value
            matl_grain_widget = self.app.report_tab.repair_grain_value 
            matl_stock_widget = self.app.report_tab.repair_tstock
            matl_condition_widget = self.app.report_tab.repair_cond_value
        else:
            matl_type_widget = self.app.report_tab.print_matl_box
            matl_subtype_widget = self.app.report_tab.print_matl_value
            matl_form_widget = self.app.report_tab.print_form_value
            matl_grain_widget = self.app.report_tab.print_grain_value 
            matl_stock_widget = self.app.report_tab.print_tstock
            matl_condition_widget = self.app.report_tab.print_cond_value
        matl_finish_widget = self.app.report_tab.findChild(QComboBox, 'Surface Finish')
        matl_coating_widget = self.app.report_tab.findChild(QComboBox, 'Surface Coating')
        
        self.setQcomboboxIndex(matl_type_widget, matl_type)
        self.setQcomboboxIndex(matl_subtype_widget, matl_subtype)
        self.setQcomboboxIndex(matl_form_widget, matl_form)
        self.setQcomboboxIndex(matl_grain_widget, matl_grain)
        self.enterField(matl_stock_widget, matl_stock)
        self.setQcomboboxIndex(matl_finish_widget, matl_finish)
        self.setQcomboboxIndex(matl_coating_widget, matl_coating)
        self.setQcomboboxIndex(matl_condition_widget, matl_condition)

    def verifyCorrectionFactors(self, fsg, fg, ft, fsf, fsc, repair=False, delta=1e-3):
        """
        Verify correction factors Fsg, Fg, Ft, Fsf, Fsc.

        Parameters
        ----------
        fsg : float
            Fsg value.
        fg : float
            Fg value.
        ft : float
            Ft value.
        fsf : float
            Fsf value.
        fsc : float
            Fsc value.
        repair : bool, optional
            Repair or print values. The default is False.
        delta : float, optional
            assertAlmostEqual delta arg. The default is 1e-3.

        Returns
        -------
        None.

        """
        if repair:
            fsg_value = float(self.app.report_tab.repair_fsg_value.text())
            fg_value = float(self.app.report_tab.repair_fg_value.text())
            ft_value = float(self.app.report_tab.repair_ft_value.text())
            fsf_value = float(self.app.report_tab.repair_fsf_value.text())
            fsc_value = float(self.app.report_tab.repair_fsc_value.text())
        else:
            fsg_value = float(self.app.report_tab.print_fsg_value.text())
            fg_value = float(self.app.report_tab.print_fg_value.text())
            ft_value = float(self.app.report_tab.print_ft_value.text())
            fsf_value = float(self.app.report_tab.print_fsf_value.text())
            fsc_value = float(self.app.report_tab.print_fsc_value.text())
        
        self.assertAlmostEqual(fsg_value, fsg, delta=delta)
        self.assertAlmostEqual(fg_value, fg, delta=delta)
        self.assertAlmostEqual(ft_value, ft, delta=delta)
        self.assertAlmostEqual(fsf_value, fsf, delta=delta)
        self.assertAlmostEqual(fsc_value, fsc, delta=delta)

    def interpolateKtdls(self, kckt_one, kckt_half, kckt_zero):
        """
        Interpolate E/F/G KtDLS.

        Parameters
        ----------
        kckt_one : float
            KtDLS at Kc/Kt = 1.0.
        kckt_half : float
            KtDLS at Kc/Kt = 0.5.
        kckt_zero : float
            KtDLS at Kc/Kt = 0.0.

        Returns
        -------
        None.

        """
        self.enterField(self.app.report_tab.kckt_one, kckt_one)
        self.enterField(self.app.report_tab.kckt_half, kckt_half)
        self.enterField(self.app.report_tab.kckt_zero, kckt_zero)

    def verifyMargin(self, fkts, ktsadj, margin, repair=False, delta=1e-3):
        """
        Verify margin of safety values Fkts, KtS-adjusted, margin of safety.

        Parameters
        ----------
        fkts : float
            KtS correction factor.
        ktsadj : float
            KtS-adjusted.
        margin : float
            Margin of safety.
        repair : bool, optional 
            Repair or Print. The default is False.
        delta : float, optional 
            assertAlmostEqual delta arg. The default is 1e-3.

        Returns
        -------
        None.

        """
        if repair:
            fkts_widget = self.app.report_tab.repair_fkts
            ktsadj_widget = self.app.report_tab.repair_kts_adj
            mos_widget = self.app.report_tab.repair_mos
        else:
            fkts_widget = self.app.report_tab.print_fkts
            ktsadj_widget = self.app.report_tab.print_kts_adj
            mos_widget = self.app.report_tab.print_mos
            
        self.assertAlmostEqual(float(fkts_widget.text()), fkts, delta=delta)
        self.assertAlmostEqual(float(ktsadj_widget.text()), ktsadj, delta=delta)
        self.assertAlmostEqual(float(mos_widget.text()), margin, delta=delta)

    def document_csv(self, title, header, data):
        """
        Document test output. 
        
        Writes to self.fp - 'tests/test_output.csv'.
        
        Parameters
        ----------
        title : str 
            Test name, table title. 
        header : list or tuple 
            Sequence of header/columns names. 
        data : list or tuple 
            Sequence of test results. 
        
        Returns 
        -------
        None. 
        
        """
        assert isinstance(title, str)
        try: 
            data[0][0]
        except TypeError:
            assert len(data) == len(header)
            write_data = (
                (title, ),
                header,
                data,
                )
        else:
            assert all([len(row) == len(header) for row in data])
            write_data = (
                (title, ),
                header,
                *data,
                )
        
        self.writer.writerows(write_data)
    
    def test_set_reference(self):
        """
        Test set_reference method. Tests for every reference system.
        
        StressCheck application 3.5 library lists 0 as an entry - no reference 
        system - but this not applicable, results in error.

        Returns
        -------
        None.

        """
        ref_map = {
            0: 'refNone',
            1: 'ref2D',
            2: 'refAxisymmetic',
            3: 'refPlate',
            4: 'ref3D',
            5: 'refExtrude',
            }
        
        app, doc, model = self.open_model('satellite-hole')
        
        # Integer Based 
        refs = []
        for i in ref_map.keys():
            self.app.set_reference(model, i)
            self.assertEqual(model.Reference, i)
            refs.append([i, model.Reference])
        
        # String Based 
        for ref in ref_map.values():
            self.app.set_reference(model, ref)
            self.assertEqual(model.Reference, i)
            refs.append([ref, model.Reference])
        
        ## 
        print('###### test_set_reference ######')
        print('Reference, StressCheck Reference')
        for x, y in refs:
            print(f'{x}, {y}')
            
        # Document 
        self.document_csv(
            'test_set_referene',
            ('Reference', 'StressCheck Reference'),
            refs,
            )
    
    def test_add_parameters(self):
        """
        Test add_parameters method.

        Returns
        -------
        None.

        """
        app, doc, model = self.open_model('satellite-hole')
        coupon = self.app.input_tab.coupon
        parameters = doc.Info.Parameters
        
        names = [parameters.ItemAtIndex(i).Name for i in range(parameters.Count)]
        for name in names:
            print(name, parameters.Parameter(name).Current)
        
        self.app.add_parameters(doc, coupon)
        names = [parameters.ItemAtIndex(i).Name for i in range(parameters.Count)]
        names.remove('s')
        for name in names:
            ## 
            # print(name, parameters.Parameter(name).Current, getattr(coupon, name))
            self.assertEqual(parameters.Parameter(name).Current, getattr(coupon, name))
        
    def test_add_points(self):
        """Test add_points."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model('satellite-hole')
        coupon = self.app.input_tab.coupon
        self.set_reference(model, ref_sys='ref2D')
        self.add_parameters(doc, coupon)
        
        # Create Points
        point_nums = self.add_points(
            model, 
            coupon
            )
        
        # Verify Points 
        point_attrs = (
            'Number',
            'Status',
            'Type',
            'Location',
            )
        point_attr_data = [[getattr(model.Points.Point(n), attr) for attr in point_attrs] for n in point_nums]
        
        ## 
        print('###### test_add_points #####')
        print(','.join(point_attrs))
        for point_attr in point_attr_data:
            ## 
            print(','.join([str(attr) for attr in point_attr]))
        
        # Document 
        self.document_csv(
            'test_add_points',
            point_attrs,
            point_attr_data
            )
        
        # Export Model 
        model.Export(os.path.abspath('tests/scw/test_add_points.scw'))
        
    def test_add_lines(self):
        """Test add_lines."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_parameters.scw'
            )
        coupon = self.app.input_tab.coupon
        self.set_reference(model, ref_sys='ref2D')
        self.add_parameters(doc, coupon)
        
        # Add Lines 
        point_nums = self.add_points(
            model, 
            coupon
            )
        line_nums = self.add_lines(
            model,
            point_nums
            )
            
        # Verify Lines 
        line_attrs = (
            'Number',
            'Name',
            'DataType',
            'Type',
            'LengthParametric',
            'LengthConstant',
            )
        line_attr_data = [[getattr(model.Lines.Line(n), attr) for attr in line_attrs] for n in line_nums]
        
        ## 
        print('###### test_add_lines ######')
        print(','.join(line_attrs))
        for line_attr in line_attr_data:
            print(','.join([str(attr) for attr in line_attr]))
        
        # Document 
        self.document_csv(
            'test_add_lines',
            line_attrs,
            line_attr_data
            )
        
    def test_add_plane(self): 
        """Test add_plane."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model('satellite-hole')
        coupon = self.app.input_tab.coupon
        self.set_reference(model, ref_sys='ref2D')
        self.add_parameters(doc, coupon)
        
        # Add Plane 
        point_nums = self.add_points(
            model, 
            coupon
            )
        plane_num = self.add_plane(
            model, 
            point_nums[0:3]
            )
        
        # Verify Plane  
        plane_attrs = (
            'Number',
            'Name',
            'DataType',
            'Type',
            'WidthParametric',
            'WidthConstant',
            'HeightParametric',
            'HeightConstant',
            )
        plane_attr = [getattr(model.Planes.Plane(plane_num), attr) for attr in plane_attrs]
        
        ## 
        print('###### test_add_plane ######')
        print(','.join(plane_attrs))
        print(','.join([str(attr) for attr in plane_attr]))
        
        # Document 
        self.document_csv(
            'test_add_plane',
            plane_attrs,
            [str(attr) for attr in plane_attr]
            )
        
        # Export Model 
        model.Export(os.path.abspath('tests/scw/test_add_plane.scw'))
        
    def test_add_systems(self): 
        """Test add_systems."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_plane.scw'
            )
        coupon = self.app.input_tab.coupon 
        
        # Create Systems
        sys_nums, surf_nums, tool_nums = self.add_systems(
            model, 
            coupon
            )
            
        ## 
        print(f'sys_nums for test_add_traction_loads, test_add_constraints')
        print(sys_nums) 
        
        # Verify Systems 
        sys_attrs = (
            'Number',
            'Status',
            'Method',
            'Location',
            'Rotation',
            'Type',
            )
        
        sys_attr_data = [[getattr(model.Systems.System(n), attr) for attr in sys_attrs] for n in sys_nums]
            
        ## 
        print('###### test_add_system ######')
        print(','.join(sys_attrs))
        for n in sys_nums: 
            sys_attr = [getattr(model.Systems.System(n), attr) for attr in sys_attrs] 
            ##
            print(','.join([str(attr) for attr in sys_attr])) 
        
        # Verify CircleCurves 
        curve_attrs = (
            *surf_attrs,
            'P1MinParametric',
            'P1MinConstant',
            'P1MaxParametric',
            'P1MaxConstant',
            )
        curve_attr_data = [[getattr(model.CircleCurves.CircleCurve(n), attr) for attr in curve_attrs] for n in tool_nums]
        
         ## 
         print('###### test_add_circle_curve ######') 
         print(',',join(curve_attrs) 
         for n in tool_nums: 
            curve_attr = [getattr(model.CircleCurves.CircleCurve(n), attr) for attr in curve_attrs]
            ## 
            print(','.join([str(attr) for attr in curve_attr]))
        
        # Verify CircleSurfaces 
        surf_attrs = (
            'Number',
            'Name',
            'DataType',
            'Type',
            'SystemNumber',
            'RadiusParametric',
            'RadiusConstant',
            )
        surf_attr_data = [[getattr(model.CircleSurfaces.CircleSurface(n), attr) for attr in surf_attrs] for n in surf_nums]
        
        ## 
        print('###### test_add_circle_surface ######')
        print(','.join(surf_attrs))
        for n in surf_nums: 
            surf_attr = [getattr(model.CircleSurfaces.CircleSurface(n), attr) for attr in surf_attrs] 
            ## 
            print(','.join([str(attr) for attr in surf_attr])) 
        
        # Document 
        self.document_csv(
            'test_add_system',
            sys_attrs,
            sys_attr_data,
            )
        self.document_csv(
            'test_add_circle_curve',
            curve_attrs,
            curve_attr_data,
            )
        self.document_csv(
            'test_add_circle_surface',
            surf_attrs,
            surf_attr_data,
            )
        
    def test_add_body_imprint(self):
        """Test add_body_imprint."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model('satellite-hole')
        coupon = self.app.input_tab.coupon
        self.set_reference(model, ref_sys='ref2D')
        self.add_parameters(doc, coupon)
        
        # Add Plane 
        point_nums = self.add_points(
            model, 
            coupon
            )
        plane_num = self.add_plane(
            model, 
            point_nums[0:3]
            )
        
        # Create Systems
        sys_nums, surf_nums, tool_nums = self.add_systems(
            model, 
            coupon
            )
        
        # Add Body Imprint to Plane
        body_num = self.add_body_imprint(
            model, 
            plane_num, 
            tool_nums
            )
        
        # Verify Body Imprint 
        body_attrs = (
            'Number',
            'Name',
            'Type',
            'Method',
            'ImprintMethod',
            'Radius1aParametric',
            'Radius1aConstant',
            'Radius1bParametric',
            'Radius2aConstant',
            'Rho1Parametric',
            'Rho1Constant',
            'Rho2Parametric',
            'Rho2Constant',
            'RadiusParametric',
            'RadiusConstant',
            )
        body_attr = [getattr(model.Bodies.Body(body_num), attr) for attr in body_attrs]
        
        ## 
        print('###### test_add_body_imprint ######') 
        print(','.join(body_attrs) 
        print(','.join([str(attr) for attr in body_attr]))
        
        # Document 
        self.document_csv(
            'test_add_body_imprint',
            body_attrs,
            body_attr,
            )
        
    def test_add_body_subtract(self):
        """Test body_subtract."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model('satellite-hole')
        
        # Set Reference and Add Parameters
        self.app.set_reference(model, ref_sys='ref2D')
        coupon = self.app.input_tab.coupon 
        self.app.add_parameters(doc, coupon)
        
        # Add Plane 
        point_nums = self.add_points(
            model, 
            coupon
            )
        line_nums = self.add_lines(
            model,
            point_nums
            )
        plane_num = self.add_plane(
            model, 
            point_nums[0:3]
            )
        
        # Create Systems
        sys_nums, surf_nums, tool_nums = self.add_systems(
            model, 
            coupon
            )
        
        # Add Body Imprint to Plane
        body_num = self.add_body_imprint(
            model, 
            plane_num, 
            tool_nums
            )
        
        # Body-Subtract Circle Surfaces from Plane
        body_num = self.body_subtract(
            model, 
            body_num + 1, 
            surf_nums
            )
        
        # Verify Body Subtract 
        body_attrs = (
            'Number',
            'Name',
            'Type',
            'Method',
            'ImprintMethod',
            'Radius1aParametric',
            'Radius1aConstant',
            'Radius1bParametric',
            'Radius2aConstant',
            'Rho1Parametric',
            'Rho1Constant',
            'Rho2Parametric',
            'Rho2Constant',
            'RadiusParametric',
            'RadiusConstant',
            )
        body_attr = [getattr(model.Bodies.Body(body_num), attr) for attr in body_attrs]
        
        ## 
        print('###### test_body_subtract ######') 
        print(','.join(body_attrs) 
        print(','.join([str(attr) for attr in body_attr]))
        
        # Document 
        self.document_csv(
            'test_body_subtract',
            body_attrs,
            body_attr, 
            )
        # Export model 
        model.Export(os.path.abspath('tests/scw/test_body_subtract.scw'))
    
    def test_add_automesh(self):
        """"Test add_automesh."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model('satellite-hole')
        
        # Set Reference and Add Parameters
        self.app.set_reference(model, ref_sys='ref2D')
        coupon = self.app.input_tab.coupon 
        self.app.add_parameters(doc, coupon)
        
        # Add Plane 
        point_nums = self.add_points(
            model, 
            coupon
            )
        plane_num = self.add_plane(
            model, 
            point_nums[0:3]
            )
        
        # Create Systems
        sys_nums, surf_nums, tool_nums = self.add_systems(
            model, 
            coupon
            )
        
        # Add Body Imprint to Plane
        body_num = self.add_body_imprint(
            model, 
            plane_num, 
            tool_nums
            )
        
        # Body-Subtract Circle Surfaces from Plane
        body_num = self.body_subtract(
            model, 
            body_num + 1, 
            surf_nums
            )
        
        # Add Automesh
        self.add_automesh(
            model, 
            body_num
            )
        
        # Verify Automesh 
        mesh_attrs = (
            'Number',
            'Type',
            'Name',
            'Description',
            'Active',
            'Value',
            'IsActive',
            'SetName',
            'AutomeshType',
            )
        
        ## 
        print('###### test_add_automesh ######') 
        meshes = [model.Automeshes.ItemAtIndex(i) for i in range model.Automeshes.Count]
        print([f'index={i}, Number={mesh.Number}' for i, mesh in enumerate(meshes)])
        mesh_num = meshes[0].Number 
        mesh_attr = [getattr(model.Automeshes.Automesh(mesh_num), attr) for attr in mesh_attrs]
        print(','.join([str(attr) for atrr in mesh_attr]))
        
        # Document 
        self.document_csv(
            'test_add_automesh',
            mesh_attrs,
            mesh_attr, 
            )
        
        # Export model 
        model.Export(os.path.abspath('tests/scw/test_add_automesh.scw'))
        
    def test_add_thickness(self):
        """Test add_thickness."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            model_path='tests/scw/test_add_automesh.scw'
            )
        
        # Add Thickness
        self.add_thickness(
            model, 
            'th'
            )
        
        # Verify ThicknessAssignment
        thk_attrs = (
            'Data',
            'ThickAssignment',
            'SetName',
            'SystemNumber',
            'ThicknessDataType',
            'Theory',
            )
        thk_attr = [getattr(model.ThicknessAssignments.ThicknessAssignment(), attr) for attr in thk_attrs] 
        
        ##
        print('###### test_add_thickness ######')
        print(','.join(thk_attrs))
        print(','.join([str(attr) for attr in thk_attr])) 
        
        # Document 
        self.document_csv(
            'test_add_thickness',
            thk_attrs,
            thk_attr, 
            )
        
        # Export Model 
        model.Export(os.path.abspath('tests/scw/test_add_thickness.scw'))
        
    def test_add_material(self):
        """Test add_material."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_thickness.scw'
            )
        
        # Add Material 
        self.add_material(
            model,
            Ep='Ep,
            nu='nu'
            )        
        
        # Verify Material 
        matl_attrs = (
            'Name',
            'Description',
            'Type',
            'Units',
            'Data',
            )
        matl_attr = [getattr(model.Materials.Material('matl'), attr) for attr in matl_attrs]
        
        ## 
        print('###### test_add_material ######')
        print(','.join(matl_attrs))
        print(','.join([str(attr) for attr in matl_attr]))
        
        # Verify MaterialAssignment 
        assign_attrs = (
            'MaterialName',
            'MatAssignment',
            'SetName',
            'SystemNumber',
            'ColorName',
            'Type',
            'Data',
            'StackAssignType',
            'BaseThick',
            'Theory',
            )
        assign_attr = [getattr(model.MaterialAssignments.MaterialAssignment(), attr) for attr in assign_attrs]
        
        ## 
        print('###### test_assign_material ######')
        print(','.join(assign_attrs))
        print(','.join([str(attr) for attr in assign_attr]))
        
        # Document 
        self.document_csv(
            'test_add_material',
            matl_attrs,
            matl_attr,
            )
        self.document_csv(
            'test_assign_material',
            assign_attrs, 
            assign_attr,
            )
    
    def test_add_formulae(self):
        """Test add_formulae.""" 
        app, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_parameters.scw'
            )
        coupon = self.app.input_tab.coupon
        
        # Add Formulae 
        self.add_formulae(
            app,
            formulaes=coupon.get_formulae()
            )
        # Verify Formulae 
        formulae_names = [model.Formulae.ItemAtIndex(i).Name for i in range(model.Formulae.Count] 
        formula_attrs = (
            'Name',
            'SystemOption',
            'AngleType',
            'IsUsingConstants',
            'IsUsingSubExpressions',
            'Constants',
            'Subexpressions',
            'FormulaExpression',
            )
        
        ## 
        print('###### test_add_formulae ######')
        print(','.join(formula_attrs))
        for name in formulae_names: 
            formula_attr = [getattr(model.Formulae.Formula(name), attr) for attr in formula_attrs] 
            ## 
            print(','.join([str(attr) for attr in formula_attr]))
        
        # Document 
        formula_attr_data = [[getattr(model.Formulae.Formula(name), attr) for attr in formula_attrs] for name in formulae_names]
        self.document_csv(
            'test_add_formulae',
            formula_attrs,
            formula_attr_data,
            )
        
    def test_add_set(self):
        """Test add_set.""" 
        # Open satellite-hole model. 
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_automesh.scw'
            )
        
        edges = ('bot', 'rh', 'top', 'left')
        line_nums = {f'curve-{edge}': n for edge, n in zip(edges, range(6, 10))}
        nums = (30, 29, 28)        
        curve01_nums = {f'curve-{i}: n for i, n in enumerate(nums)} 
        nums = (33, 32, 31)        
        curve_nums = {f'curve-{i}: n for i, n in enumerate(nums)}
        
        # Add Sets
        self.add_set(
            model,
            {**curve_nums, **curve01_nums, **line_nums},
            )
        
        # Verify Sets 
        set_names = [model.Sets.ItemAtIndex(i).Name for i in range(model.Sets.Count] 
        set_attrs = (
            'Name',
            'Option',
            'Type',
            'ObjectCount',
            'ObjectList',
            'ObjectTypeList',
            'SystemNumber',
            )
        set_attr_data = [[getattr(model.Sets.Set(name), attr) for attr in set_attrs] for name in set_names]
        
        ## 
        print('###### test_add_set ######')
        print(','.join(set_attrs)) 
        for set_attr in set_attr_data:             
            ## 
            print(','.join([str(attr) for attr in set_attr]))
        
        # Document 
        self.document_csv(
            'test_add_set',
            set_attrs,
            set_attr_data,
            )
        
    def test_get_nodes(self):
        """Test get_nodes."""
        # Open satellite-hole model. 
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_automesh.scw'
            )
        coupon = self.app.input_tab.coupon 
        
        node_nums = self.get_nodes(
            model,
            coupon.w,
            coupon.h
            )
        
        # Verify Node Numbers 
        node_attrs = (
            'Number',
            'Type',
            'Location',
            )
        node_attr_data = [[getattr(model.Nodes.Node(n), attr) for attr in node_attrs] for n in node_nums]
            
        ## 
        print('###### test_get_nodes ######')
        print(','.join(node_attrs))
        for node_attr in node_attr_data:
            ## 
            print(','.join([str(attr) for attr in node_attr]))
        
        # Document 
        self.document_csv(
            'test_add_nodes',
            node_attrs,
            node_attr_data,
            )
        
    def test_add_traction_loads(self):
        """Test add_traction_loads."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_set.scw'
            )
        idxs = (*range(3), 'bot', 'left')
        nums = range(1, 6)
        sys_nums = {f'sys-{idx}: num for idx, num in zip(idxs, nums)}
        
        # Add Traction Loads 
        self.add_traction_loads(
            model, 
            sys_nums, 
            )
        
        # Verify Loads 
        load_attrs = (
            'Number',
            'Name',
            'Type',
            'SetName',
            'ObjectNumber',
            'LoadDirection',
            'SystemNum',
            'Data',
            'Method',
            'Application',
            'LoadAssignment',
            'Location',
            'Vector',
            ) 
        ##
        traction_loads = [model.Loads.Load(i) if model.Loads.Load(i).Method == 1 for in range(model.Loads.Count)]
        load_attr_data = [[getattr(load, attr) for attr in load_attrs] for load in traction_loads]
        
        ##
        print('###### test_add_traction_loads #######')
        print(','.join(load_attrs))
        for load_attr in load_attr_data:
            ## 
            print(','.join([str(attr) for attr in load_attr]))
        
        # Document 
        self.document_csv(
            'test_add_traction_loads',
            load_attrs,
            load_attr_data,
            )
        
        # Export Model 
        model.Export(os.path.abspath('test/scw/test_add_traction_loads.scw'))
        
    def test_add_bearing_loads(self):
        """Test add_bearing_loads."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_traction_loads.scw'
            )
        
        # Add Bearing Loads 
        self.add_bearing_loads(model) 
        
        # Verify Loads 
        load_attrs = (
            'Number',
            'Name',
            'Type',
            'SetName',
            'ObjectNumber',
            'LoadDirection',
            'SystemNum',
            'Data',
            'Method',
            'Application',
            'LoadAssignment',
            'Location',
            'Vector',
            'LoadBearingCorrectionOption',
            ) 
        brg_loads = [model.Loads.Load(i) if model.Loads.Load(i).Method == 6 for in range(model.Loads.Count)]
        load_attr_data = [[getattr(load, attr) for attr in load_attrs] for load in brg_loads] 
        
        ##
        print('###### test_add_traction_loads #######')
        print(','.join(load_attrs))
        for load_attr in load_attr_data: 
            ## 
            print(','.join([str(attr) for attr in load_attr]))
        
        # Document 
        self.document_csv(
            'test_add_bearing_loads',
            load_attrs, 
            load_attr_data,
            ) 
        
        # Export Model 
        model.Export(os.path.abspath('test/scw/test_add_bearing_loads.scw'))
    
    def test_add_constraints(self):
        """Test add_constraints for every constraint configuration."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_bearing_loads.scw'
            )
        idxs = (*range(3), 'bot', 'left')
        nums = range(1, 6)
        sys_nums = {f'sys-{idx}: num for idx, num in zip(idxs, nums)}        
        
        # Add Constraints
        const_flags = (
            None,
            'bot',
            'rh',
            'top',
            'lh',
            'bot-lh',
            'bot-rh',
            'lh-bot',
            'lh-top',
            'top-rh',
            'top-lh',
            'lh-top',
            'lh-bot',
            )
        const_attrs = (
            'Number',
            'Name',
            'Type',
            'SetName',
            'BoundaryNumber',
            'ConstraintDirection',
            'SystemNumber',
            'Data',
            'Method',
            'NodeNumbers',
            'ObjectType',
            )
        coupon = self.app.input_tab.coupon 
        node_nums = self.get_nodes(
            model,
            coupon.w,
            coupon.h
            )
        
        ##
        print('###### test_add_constraints ######')
        print(','.join(('Flag,') + const_flags)) 
        
        for flag for const_flags:
            const_name = self.add_constraints(
                model, 
                node_nums, 
                sys_nums,
                flags=flag
                )
            
            const_attr_data = [[getattr(model.Constraints.Constraint(i), attr) for attr in const_attrs] for i in range(model.Constraints.Count)]
            
            ##
            for const_attr in const_attr_data: 
                print(','.join([str(flag)]+[str(attr) for attr in const_attr]))
            
            # Document
            self.document_csv(
                f'test_add_constraints({flag}',
                const_attrs, 
                const_attr_data, 
                )
            
        # Export Model 
        model.Export(os.path.abspath('tests/scw/test_add_constraints.scw'))
        
    def test_add_solutionids(self) 
        """Test add_solutionids."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_constraints.scw'
            )
        
        # Add SolutionIDs 
        const_name = model.Constraints.Constraint(0).Name 
        self.add_solutionids(
            model,
            const_name
            )
        
        # Verify SolutionIDs 
        solnid_attrs = (
            'Name',
            'ConstraintName',
            'LoadName',
            'Status',
            'Type',
            )
        solnid_attr_data = [[getattr(model.SolutionIDs.ItemAtIndex(i), attr) for attr in solnid_attrs] for i in range(model.SolutionIDs.Count)]
        
        ## 
        print('###### test_add_solutionids ######') 
        print(','.join(solnid_attrs))
        for solnid_attr in solnid_attr_data:
            ##
            print(','.join([str(attr) for attr in solnid_attr]))
        
        # Document 
        self.document_csv(
            'test_add_solutionids',
            solnid_attrs, 
            solnid_attr_data, 
            )
        
        # Export Model 
        model.Export(os.path.abspath('tests/scw/test_add_solutionids.scw'))
    
    def test_add_solution(self):
        """Test add_solution."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_solutionids.scw'
            )
        
        # Add Linear Solution 
        soln_name = self.add_solution(app)
        
        # Verify 
        soln_attrs = (
            'Name',
            'Description',
            'Type',
            'Startup',
            'Iteration',
            'Convergence',
            'RunLimit',
            'PLevel',
            'PLimit',
            'Method',
            'IsSequence',
            'OptimizationPSol',
            'ConvergeMethod',
            'Reference',
            'Theory',
            'ExtractSettingName',
            )
        soln_attr = [getattr(sc.Solutions.Solution(soln_name), attr) for attr in soln_attrs] 
        
        ##
        print('###### test_add_solution ######')
        print(','.join(soln_attrs))
        print(','.join([str(attr) for attr in soln_attr]))
        
        # Document 
        self.document_csv(
            'test_add_solution',
            soln_attrs,
            soln_attr,
            )
        
        # Export model 
        model.Export(os.path.abspath('tests/scw/test_add_solution.scw'))
    
    def test_add_xerror(self):
        """Test add_xerror."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_solution.scw'
            )
        
        # Add Error Extraction
        x_name 'soln-error'
        self.add_xerror(
            app=sc,
            name=x_name,
            solnid='combined'
            )
        
        # Verify Error Extraction 
        x_attrs = (
            'Name',
            'Title',
            'Type',
            'Reference',
            'Theory',
            'SolutionID',
            'Format',
            'SetName',
            'ReportingStyle',
            'DisplayPoints',
            'RunMin',
            'RunMax',
            'Error_Method',
            'Extract_Method',
            'Error_Object',
            'ElasticityFunction',
            )
        x_attr = [getattr(doc.Extractions.Extract(x_name), attr) for attr in x_attrs] 
        
        ## 
        print('##### test_add_xerror ######') 
        print(','.join(x_attrs))
        print(','.join([str(attr) for attr in x_attr]))
        
        # Document 
        self.document_csv(
            'test_add_xerror',
            x_attrs,
            x_attr,
            )
    
    def test_add_xplot(self):
        """Test add_xplot."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_solution.scw'
            )
        
        # Add View 
        view_name = 'fringe'
        self.add_view(
            model,
            name=view_name
            )
        
        # Add xplots ey, s1, bc 
        sys_num = 1
        view_name='fringe'
        # (elasticityFunction, isFringe)
        funcs = (
            ('ey', True),
            ('s1', True),
            ('bc', False),
            )
        for func, is_fringe in funcs:
            self.add_xplot(
                app=app,
                name=func,
                solnid='combined',
                view_name=view_name,
                sys_num=sys_num,
                func=func,
                is_fringe=is_fringe,
                )
        
        # Verify 
        plot_attrs = (
            'Name',
            'Title',
            'Type',
            'Object',
            'SolutionType',
            'SolutionID',
            'RunNumber',
            'Reference',
            'Theory',
            'Shape',
            'View',
            'Strain',
            'Function',
            'SysFlag',
            'SystemNumber',
            'Midsides',
            'Format',
            'DoFringe',
            )
        plot_attr_data = [[getattr(doc.Plots.Plot(name), attr) for attr in plot_attrs] for name, _ in funcs] 
        
        ## 
        print('###### test_add_xplot ######')
        print(','.join(plot_attrs))
        for plot_attr in plot_attr_data:
            print(','.join([str(attr) for attr in plot_attr]))
        
        # Document 
        self.document_csv(
            'test_add_xplot',
            plot_attrs, 
            plot_attr_data,
            )
        
    def test_add_xminmax(self): 
        """Test add_xminmax."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_solution.scw'
            )
        
        # Add Min/Max/Avg Extraction
        x_name = 'convg-error'
        self.add_xminmax(
            sc,
            x_name,
            solnid='combined', 
            run_min=1, 
            run_max=3, 
            func='s1', 
            set_name='', 
            sys_num=0, 
            obj=42
            )
        
        # Verify 
        x_attrs = (
            'Name',
            'Title',
            'Type',
            'Reference',
            'Theory',
            'SolutionID',
            'Format',
            'SetName',
            'ReportingStyle',
            'DisplayPoints',
            'RunMin',
            'RunMax',
            'MinMax_Min',
            'MinMax_Max',
            'Extract_Method',
            'MinMax_LocateMax',
            'MinMax_Midsides',
            'ElasticityFunction',
            )
        x_attr = [getattr(doc.Extractions.Extract(x_name), attr) for attr in x_attrs] 
        
        ## 
        print('##### test_add_xminmax ######') 
        print(','.join(x_attrs))
        print(','.join([str(attr) for attr in x_attr]))
        
        # Document 
        self.document_csv(
            'test_add_xminmax',
            x_attrs,
            x_attr,
            )
        
    def test_add_xpoint(self): 
        """Test add_xpoint."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_solution.scw'
            )
        idxs = (*range(3), 'bot', 'left')
        nums = range(1, 6)
        sys_nums = {f'sys-{idx}: num for idx, num in zip(idxs, nums)}
        
        # Add Point Extractions
        curve_nums = (f'curve-{i}' for i in range(3))
        curve01_nums = (f'curve01-{i}' for i in range(3))
        xnames = (
            'byp-pos-ey',
            'byp-neg-ey',
            'brg-pos-ey',
            'brg-neg-ey',
            's1',
            )
        solnid_map = {
            'byp-pos-ey': 'byp-pos',
            'byp-neg-ey': 'byp-neg',
            'brg-pos-ey': 'brg-pos',
            'brg-neg-ey': 'brg-neg',
            's1': 'combined',
            's101': 'combined',
            }
        
        # At Hole Wall 
        x_names = []
        for set_name in curve_nums:
            i = set_name.split('-')[-1]
            for name in xnames:
                if name.endswith('ey'):
                    func = 'ey'
                else:
                    func = name
                x_name = f'{name}-{i}'
                x_names.append(x_name)
                self.add_xpoint(
                    sc,
                    x_name,
                    set_name=set_name,
                    sys_num=sys_nums.get(f'sys-{i}', 0),
                    solnid=solnid_map.get(name, 'combined'),
                    func=func
                    )
        
        # At 0.01" from Hole Wall
        for set_name in curve01_nums:
            i = set_name.split('-')[-1]
            x_name = f's101-{i}'
            x_names.append(x_name)
            self.add_xpoint(
                sc,
                x_name,
                set_name=set_name,
                sys_num=sys_nums.get(f'sys-{i}', 0),
                )
    
        # Verify 
        x_attrs = (
            'Name',
            'Title',
            'Type',
            'Reference',
            'Theory',
            'SolutionID',
            'Format',
            'SetName',
            'ReportingStyle',
            'DisplayPoints',
            'RunMin',
            'RunMax',
            'Extract_Method',
            'SystemNumber',
            'SysFlag',
            'Strain',
            'Points_Object',
            'Points_NumberOfPoints',
            'ElasticityFunction',
            )
        x_attr_data = [[getattr(doc.Extractions.Extract(x_name), attr) for attr in x_attrs] for x_name in x_names]
        
        ## 
        print('##### test_add_point ######') 
        print(','.join(x_attrs))
        for x_attr in x_attr_data:
            print(','.join([str(attr) for attr in x_attr]))
        
        # Document 
        self.document_csv(
            'test_add_xpoint',
            x_attrs,
            x_attr_data,
            )
    
    def test_add_view(self):
        sc, doc, model = self.open_model(
            'satellite-hole',
            ) 
        
        # Add View 
        view_name = 'fringe'
        self.add_view(
            model,
            name=view_name
            )
        
        # Verify 
        view_attrs = (
            'Name',
            'CameraX',
            'CameraY',
            'CameraZ',
            'TargetX',
            'TargetY',
            'TargetZ',
            'UpVectorX',
            'UpVectorY',
            'UpVectorZ',
            'Width',
            'Height',
            'AutoCenter',
            )
        view_attr = [getattr(model.Display.Views.View(view_name), attr) for attr in view_attrs] 
        
        ## 
        print('###### test_add_view ######')
        print(','.join(view_attrs))
        print(','.join([str(attr) for attr in view_attr])) 
        
        # Document 
        self.document_csv(
            'test_add_view',
            view_attrs,
            view_attr,
            )
    
    def test_add_label(self):
        """Test add_label for rivet-a on satellite-hole model."""
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_automesh.scw'
            )
        
        # Add Label
        label_num = self.add_label(
            model,
            label='a',
            x='x1',
            y='y1'
            )
        
        # Verify 
        label_attrs = (
            'Number',
            'Status',
            'Type',
            'Text',
            'Location',
            'FontName',
            'FontSize',
            'FontStyle',
            'FontUnderline',
            'FontStrikeout',
            'Offset',
            'FontColor',
            )
        label_attr = [getattr(model.Labels.Label(label_num), attr) for attr in label_attrs]
        
        ##
        print('###### test_add_label ######')
        print(','.join(label_attrs))
        print(','.join([str(attr) for attr in label_attr]))
        
        # Document 
        self.document_csv(
            'test_add_label',
            label_attrs,
            label_attr,
            )
    
    def test_add_lif_extraction(self):
        """Test add_lif_extraction.""" 
        sc, doc, model = self.open_model(
            'satellite-hole',
            'tests/scw/test_add_solution.scw'
            )
            
        dia = 0.2550
        r_dia = 0.3281
        
        # Add Print Geometry
        self.setPrintGeometrySatelliteHole(
            x0=0.492,
            y0=0.9275,
            d0=dia,
            x1=0.492,
            y1=0.9275,
            d1=0.255,
            x2=0.492,
            y2=0.9275,
            d2=0.255,
            w=1.5425,
            h=1.855,
            th=0.25,
            Ep=10.3,
            Ef0=30.0,
            Ef1=30.0,
            Ef2=30.0,
            csk0=0,
            csk1=0,
            csk2=0,
            nf=False,
            )
        
        # Add Repair Geometry
        self.setRepairGeometrySatelliteHole(
            d0=r_dia,
            d1=0.3281,
            d2=0.3281,
            th=0.235,
            Ef0=30.0,
            Ef1=30.0,
            Ef2=30.0,
            csk0=0,
            csk1=0,
            csk2=0,
            nf=False,
            )
        
        # Add Loads
        self.setBypassLoad(fy_byp=9809)
        self.setBearingAxialLoad(px_neg=104)
        self.setBearingShearLoad(vbs_rh_neg=1289)
        
        # Solve
        self.clickObject(self.app.input_tab.solve_btn)
        self.assertFalse(self.app.input_tab.solve_btn.isEnabled())
        
        # Wait for finished signal
        finished = QSignalSpy(self.app.worker_signals.finished)
        finished.wait(timeout=120000)  # ms
        
        # Get Extraction 
        r_dia = 
        mid, fay = self.add_lif_extraction(
            sc, 
            r_dia, 
            sys_num=1, 
            set_name='curve-repair',
            clear_extract=False
            )
        
        # Verify 
        x_attrs = (
            'Name',
            'Title',
            'Type',
            'Reference',
            'Theory',
            'SolutionID',
            'Format',
            'SetName',
            'ReportingStyle',
            'DisplayPoints',
            'RunMin',
            'RunMax',
            'Extract_Method',
            'SystemNumber',
            'SysFlag',
            'Strain',
            'Points_Object',
            'Points_NumberOfPoints',
            'ElasticityFunction',
            )
        x_names = (
            'brg-pos-ey-cil', 
            'byp-pos-ey-cil', 
            'brg-neg-ey-cil',
            'byp-neg-ey-cil',
            )
        x_attr_data = [[getattr(doc.Extractions.Extract(x_name), attr) for attr in x_attrs] for x_name in x_names]
        
        ## 
        print('##### test_add_lif_extraction ######') 
        print(','.join(x_attrs))
        for x_attr in x_attr_data:
            print(','.join([str(attr) for attr in x_attr]))
        
        # Document 
        self.document_csv(
            'test_add_lif_extraction',
            x_attrs,
            x_attr_data,
            )
        
        # Save Model 
        model.Export(os.path.abspath('tests/scw/test_add_lif_extraction.scw'))
    
    def test_file_save_analysis(self, fname=r'tests\pkl\test.pkl'):
        """
        Test file_save_analysis.

        Parameters
        ----------
        fname : str, optional
            Save-as file name. The default is tests\pkl\test.pkl.

        Returns
        -------
        None.

        """
        if self.app.tabs.count() == 1:
            # Select Model
            self.clickObject(self.app.satellitehole_model, Qt.LeftButton)
            self.assertEqual(self.app.input_tab.objectName(), 'satellite-hole')
        
        try:
            self.assertFalse(os.path.exists(fname))
        except AssertionError:
            os.remove(fname)
        
        self.app.file_save_analysis(fname)
        self.assertTrue(os.path.exists(fname))

    def test_file_save_model(self, fname=r'tests\scw\test'):
        """
        Test file_save_analysis method.

        Parameters
        ----------
        fname : str, optional
            Filename and path. The default is r'tests\scw\test'.

        Returns
        -------
        None.

        """
        scw_dir = r'tests/scw'
        if self.app.tabs.count() < 3: 
            pass 
        else:
            file_count = len([f for f in os.listdir(scw_dir)])
            self.app.file_save_model(fname)
            self.assertTrue(file_count < len([f for f in os.listdir(scw_dir)]))
    
    def test_file_load_analysis(self, fname=r'tests\pkl\req-00057114-holes-8to18.pkl'): 
        """
        Test file_load_analysis. 

        Parameters
        ----------
        fname : str, optional
            pkl filename and path.

        Returns
        -------
        None.

        """
        self.assertTrue(os.path.exists(fname) and fname.endswith('.pkl'))
        self.app.file_load_analysis(fname)
        
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        self.assertEqual(self.app.input_tab.coupon.x0, 0.492)
        self.assertEqual(self.app.input_tab.coupon.Px, -104.0)
    
    def test_check_sym_const(self):
        """
        Test all symmetric bearing constraint configuration and rigid body.

        Returns
        -------
        None.

        """
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Configure WorkerSignals
        self.app.worker_signals = main.WorkerSignals()
        
        # Set Coupon Geometry
        dia = 1
        w = h = 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            w=w,
            h=h,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # 'bot'
        # +py
        self.setBearingAxialLoad(py_pos=1)
        self.assertEqual(self.app._check_sym_const(), 'bot')
        # vbs_lh_neg
        self.setBearingAxialLoad()
        self.setBearingShearLoad(vbs_lh_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot')
        # vbs_rh_neg
        self.setBearingShearLoad(vbs_rh_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot')
        
        # 'bot-lh'
        # +py, +px
        self.setBearingAxialLoad(py_pos=1, px_pos=1)
        self.setBearingShearLoad()
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # +py, vbs_bot_neg
        self.setBearingAxialLoad(py_pos=1)
        self.setBearingShearLoad(vbs_bot_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # +py, vbs_top_neg
        self.setBearingAxialLoad(py_pos=1)
        self.setBearingShearLoad(vbs_top_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # vbs_lh_neg, +px
        self.setBearingAxialLoad(px_pos=1)
        self.setBearingShearLoad(vbs_lh_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # vbs_lh_neg, vbs_bot_neg
        self.setBearingAxialLoad()
        self.setBearingShearLoad(vbs_lh_neg=1, vbs_bot_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # vbs_lh_neg, vbs_top_neg
        self.setBearingShearLoad(vbs_lh_neg=1, vbs_top_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # vbs_rh_neg, +px
        self.setBearingAxialLoad(px_pos=1)
        self.setBearingShearLoad(vbs_rh_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # vbs_rh_neg, vbs_bot_neg
        self.setBearingAxialLoad()
        self.setBearingShearLoad(vbs_rh_neg=1, vbs_bot_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # vbs_rh_neg, vbs_top_neg
        self.setBearingShearLoad(vbs_rh_neg=1, vbs_top_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        
        # 'bot-rh'
        # +py, -px
        self.setBearingAxialLoad(py_pos=1, px_neg=1)
        self.setBearingShearLoad()
        self.assertEqual(self.app._check_sym_const(), 'bot-rh')
        # vbs_lh_neg, -px
        self.setBearingAxialLoad(px_neg=1)
        self.setBearingShearLoad(vbs_lh_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-rh')
        # vbs_rh_neg, -px
        self.setBearingAxialLoad(px_neg=1)
        self.setBearingShearLoad(vbs_rh_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'bot-rh')
        
        # 'top'
        # -Py
        self.setBearingAxialLoad(py_neg=1)
        self.setBearingShearLoad()
        self.assertEqual(self.app._check_sym_const(), 'top')
        
        # 'top-lh'
        # -py, +px
        self.setBearingAxialLoad(py_neg=1, px_pos=1)
        self.assertEqual(self.app._check_sym_const(), 'top-lh')
        # -py, vbs_bot_neg
        self.setBearingAxialLoad(py_neg=1)
        self.setBearingShearLoad(vbs_bot_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'top-lh')
        # -py, vbs_top_neg
        self.setBearingAxialLoad(py_neg=1)
        self.setBearingShearLoad(vbs_top_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'top-lh')
        
        # 'top-rh'
        # -py, -px
        self.setBearingAxialLoad(py_neg=1, px_neg=1)
        self.setBearingShearLoad()
        self.assertEqual(self.app._check_sym_const(), 'top-rh')
        
        # 'lh'
        # +px
        self.setBearingAxialLoad(px_pos=1)
        self.assertEqual(self.app._check_sym_const(), 'lh')
        # vbs_bot_neg
        self.setBearingAxialLoad()
        self.setBearingShearLoad(vbs_bot_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'lh')
        # vbs_top_neg
        self.setBearingShearLoad(vbs_top_neg=1)
        self.assertEqual(self.app._check_sym_const(), 'lh')
        
        # 'rh'
        # -px
        self.setBearingAxialLoad(px_neg=1)
        self.setBearingShearLoad()
        self.assertEqual(self.app._check_sym_const(), 'rh')
        
        # Corner 
        self.app.reset_loads()
        pos = QPoint(2, self.app.input_tab.corner_check.height()/2)
        self.clickObject(self.app.input_tab.corner_check, pos=pos)
        self.assertTrue(self.app.input_tab.corner_check.isChecked())
        # 'bot-lh'
        self.clickObject(self.app.input_tab.byp_button)
        self.assertTrue(self.app.input_tab.byp_button.isChecked())
        self.assertEqual(self.app._check_sym_const(), 'bot-lh')
        # 'top-lh'
        self.clickObject(self.app.input_tab.axial_shear_button)
        self.assertTrue(self.app.input_tab.axial_shear_button.isChecked())
        self.assertEqual(self.app._check_sym_const(), 'top-lh')
        # 'top-rh'
        self.clickObject(self.app.input_tab.brg_axial_button)
        self.assertTrue(self.app.input_tab.brg_axial_button.isChecked())
        self.assertEqual(self.app._check_sym_const(), 'top-rh')
        # 'bot-rh'
        self.clickObject(self.app.input_tab.brg_shear_button)
        self.assertTrue(self.app.input_tab.brg_shear_button.isChecked())
        self.assertEqual(self.app._check_sym_const(), 'bot-rh')
        
        # Rigid body - Standard Loads
        pos = QPoint(2, self.app.input_tab.corner_check.height()/2)
        self.clickObject(self.app.input_tab.corner_check, pos=pos)
        self.assertFalse(self.app.input_tab.corner_check.isChecked())
        # Bypass 
        self.setBypassLoad(fx_byp=1, v_byp=1)
        self.assertTrue(self.app._check_sym_const() is None)
        # Axial-Shear 
        self.setAxialShearLoad(v_bot_neg=1, v_rh_pos=1)
        self.assertTrue(self.app._check_sym_const() is None)

    def test_set_model_params_singlehole(self):
        """
        Test set_model_params.
        
        Implicitly tests open_sc_model.

        Returns
        -------
        None.

        """
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Configure callback
        self.app.worker_signals = main.WorkerSignals()
        
        # Open StressCheck
        sc, doc, model = self.app.open_sc_model(
            self.app.worker_signals.progress,
            self.app.ctx.single_hole_model
            )
        
        # Set Geometry
        dia = 0.75
        w , h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            w=w,
            h=h,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_neg=858)
        self.setBearingShearLoad(vbs_rh_neg=92106)
        
        # Coupon Parameters
        params = [
            ('d0', )*2,
            ('x0', )*2,
            ('y0', )*2,
            ('w', )*2,
            ('h', )*2,
            ('th', )*2,
            ('Ep', )*2,
            ('nu', )*2,
            ('Fx_bot_brg', )*2,
            ('Fx_bot_byp', )*2,
            ('Fx_lh_brg', )*2,
            ('Fx_lh_byp', )*2,
            ('Fx_rh_brg', )*2, 
            ('Fx_rh_byp', )*2,
            ('Fx_top_brg', )*2,
            ('Fx_top_byp', )*2,
            ('Fy_bot_brg', )*2,
            ('Fy_bot_byp', )*2,
            ('Fy_lh_brg', )*2,
            ('Fy_lh_byp', )*2,
            ('Fy_rh_brg', )*2,
            ('Fy_rh_byp', )*2,
            ('Fy_top_brg', )*2,
            ('Fy_top_byp', )*2,
            ('M_bot_brg', )*2,
            ('M_bot_byp', )*2,
            ('M_lh_brg', )*2,
            ('M_lh_byp', )*2,
            ('M_rh_brg', )*2,
            ('M_rh_byp', )*2,
            ('M_top_brg', )*2,
            ('M_top_byp', )*2,
            ('Px', )*2,
            ('Py', )*2,
            ]
        self.app.set_model_params(
            doc,
            self.app.input_tab.coupon,
            params, 
            self.app.worker_signals.progress
            )
        
        # Verify Parameters
        delta = 1e-3
        pnames = [p.lower() for p, _ in params]
        for i in range(doc.Info.Parameters.Count):
            p = doc.Info.Parameters.ItemAtIndex(i)
            if p.Name.lower() in pnames:
                try:
                    value = getattr(self.app.input_tab.coupon, p.Name)
                except AttributeError:
                    value = getattr(self.app.input_tab.coupon, p.Name.capitalize())
                
                self.assertAlmostEqual(
                    p.Current, 
                    value,
                    delta=delta
                    )
        
        # Close sc
        sc.Close()
        doc, model = None, None
    
    def test_set_model_params_satellitehole(self):
        """
        Test set_model_params on satellite-hole model.
        
        Returns
        -------
        None.

        """
        sc, doc, model = self.open_model('satellite-hole')
        
        # Set Geometry
        dia = 0.75
        w , h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            x1=w/4,
            y1=h/4,
            d1=dia/4,
            x2=3*w/4,
            y2=3*h/4,
            d2=dia/4,
            w=w,
            h=h,
            th=0.1314,
            Ep=16.0,
            Ef=30.0,
            nf=True,
            csk_depth=0.036
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_neg=858)
        self.setBearingShearLoad(vbs_rh_neg=92106)
        
        # Coupon Parameters
        params = [
            ('d0', )*2,
            ('x0', )*2,
            ('y0', )*2,
            ('w', )*2,
            ('h', )*2,
            ('th', )*2,
            ('Ep', )*2,
            ('nu', )*2,
            ('Fx_bot_brg', )*2,
            ('Fx_bot_byp', )*2,
            ('Fx_lh_brg', )*2,
            ('Fx_lh_byp', )*2,
            ('Fx_rh_brg', )*2, 
            ('Fx_rh_byp', )*2,
            ('Fx_top_brg', )*2,
            ('Fx_top_byp', )*2,
            ('Fy_bot_brg', )*2,
            ('Fy_bot_byp', )*2,
            ('Fy_lh_brg', )*2,
            ('Fy_lh_byp', )*2,
            ('Fy_rh_brg', )*2,
            ('Fy_rh_byp', )*2,
            ('Fy_top_brg', )*2,
            ('Fy_top_byp', )*2,
            ('M_bot_brg', )*2,
            ('M_bot_byp', )*2,
            ('M_lh_brg', )*2,
            ('M_lh_byp', )*2,
            ('M_rh_brg', )*2,
            ('M_rh_byp', )*2,
            ('M_top_brg', )*2,
            ('M_top_byp', )*2,
            ('Px', )*2,
            ('Py', )*2,
            ]
        self.app.set_model_params(
            doc,
            self.app.input_tab.coupon,
            params, 
            self.app.worker_signals.progress
            )
        
        # Verify Parameters
        delta = 1e-3
        pnames = [p.lower() for p, _ in params]
        for i in range(doc.Info.Parameters.Count):
            p = doc.Info.Parameters.ItemAtIndex(i)
            if p.Name.lower() in pnames:
                try:
                    value = getattr(self.app.input_tab.coupon, p.Name)
                except AttributeError:
                    value = getattr(self.app.input_tab.coupon, p.Name.capitalize())
                ##
                print(p.Name, value, p.Current)
                ##
                self.assertAlmostEqual(
                    p.Current, 
                    value,
                    delta=delta
                    )
        
        # Close sc
        sc.Close()
        doc, model = None, None
    
    def test_singlehole_add_loads(self):
        """
        Test _singlehole_add_loads method.
        
        Verifies for all constraint flags and load Type, SetName, ObjectNumber,
        LoadDirection, SystemNum, Data, Method.
        

        Returns
        -------
        None.

        """
        # Get pickled verification data
        with open('tests/pkl/singlehole_add_loads.pkl', 'rb') as fp:
            data = pickle.load(fp)
        
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Configure callback
        self.app.worker_signals = main.WorkerSignals()
        
        # Open StressCheck
        sc, doc, model = self.app.open_sc_model(
            self.app.worker_signals.progress,
            self.app.ctx.single_hole_model
            )
        
        # Set Geometry
        dia = 0.75
        w , h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            w=w,
            h=h,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_neg=858)
        self.setBearingShearLoad(vbs_rh_neg=92135)
        
        # Add Loads
        sym_flags = (
            None,
            'top', 
            'bot', 
            'lh', 
            'rh',
            'top-rh',
            'top-lh',
            'bot-rh',
            'bot-lh'
            )
        loads = model.Loads
        for flag in sym_flags:
            self.app._singlehole_add_loads(
                model,
                flag
                )
            
            # Verify 
            load = loads.Load(0)
            self.assertEqual(data[flag]['type'], load.Type)
            self.assertEqual(data[flag]['set'], load.SetName)
            self.assertEqual(data[flag]['obj'], load.ObjectNumber)
            self.assertEqual(data[flag]['direction'], load.LoadDirection)
            self.assertEqual(data[flag]['sys'], load.SystemNum)
            self.assertEqual(data[flag]['data'][0], load.Data(1)[0])
            self.assertEqual(data[flag]['data'][1], load.Data(1)[1])
            self.assertEqual(data[flag]['method'], load.Method)
            
            # Reset Loads
            loads.Clear()
            model.Sets.Clear()
        
        # Close SC
        sc.Close()
        doc, model = None, None
    
    def test_singlehole_add_constraints(self):
        """
        Test singlehole_add_constraints method.
        
        Returns
        -------
        None.

        """
        # Get pickled verification data
        with open('tests/pkl/singlehole_add_constraints.pkl', 'rb') as fp:
            data = pickle.load(fp)
        
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Configure callback
        self.app.worker_signals = main.WorkerSignals()
        
        # Open StressCheck
        sc, doc, model = self.app.open_sc_model(
            self.app.worker_signals.progress,
            self.app.ctx.single_hole_model
            )
        
        # Add Constraints
        sym_flags = (
            None,
            'top', 
            'bot', 
            'lh', 
            'rh',
            'top-rh',
            'top-lh',
            'bot-rh',
            'bot-lh'
            )
        results = {}
        for flag in sym_flags:
            name = self.app._singlehole_add_constraints(
                model,
                flag
                )
            
            # Verify
            const = model.Constraints.Constraint(0)
            self.assertEqual(const.Name, name)
            self.assertEqual(data[flag]['Name'], const.Name)
            self.assertEqual(data[flag]['Type'], const.Type)
            self.assertEqual(
                data[flag]['ConstraintDirection'], 
                const.ConstraintDirection
                )
            self.assertEqual(data[flag]['SystemNumber'], const.SystemNumber)
            if const.Type == 0:
                self.assertEqual(data[flag]['Data'][0], const.Data(0)[0])
            self.assertEqual(data[flag]['Method'], const.Method)
            self.assertEqual(data[flag]['ObjectType'], const.ObjectType)
            
            # Clear Constraints
            model.Constraints.Clear()
    
    # def test_set_traction_loads(self):
    #   pass
    
    # def test_set_bearing_loads(self):
    #   pass
    
    # def test_set_constraints(self):
    #   pass

    def test_singlehole_soln_params(self):
        """
        Test _singlehole_soln_params.
        
        Verifies keys 'model', 'soln', 'fringe', and 'params'. _check_sym_const
        or 'flags' tested separately.

        Returns
        -------
        None.

        """
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Configure callback
        self.app.worker_signals = main.WorkerSignals()
        
        # Open StressCheck
        sc, doc, model = self.app.open_sc_model(
            self.app.worker_signals.progress,
            self.app.ctx.single_hole_model
            )
        
        # Set Geometry
        dia = 0.805
        w , h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            w=w,
            h=h,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_pos=858)
        self.setBearingShearLoad(vbs_rh_neg=92135)
        
        # Get parameters
        print_params = self.app._singlehole_soln_params()
        repair_params = self.app._singlehole_soln_params(repair=True)
        
        # model
        self.assertEqual(print_params['model'], self.app.ctx.single_hole_model)
        self.assertEqual(repair_params['model'], self.app.ctx.single_hole_model)
        
        # flags
        self.assertEqual(print_params['flags'], 'bot-lh')
        self.assertEqual(print_params['flags'], 'bot-lh')
        
        # fringe 
        for soln, params in zip(('print', 'repair'), (print_params, repair_params)):
            keys = (
                f's1-{soln}',
                f'ey-{soln}',
                f's1-local-{soln}',
                'bc',
                )
            self.assertTrue(all([key in params['fringe'].keys() for key in keys]))
            
            fringe_map = zip(
                (
                    params['fringe'][f's1-{soln}'],
                    params['fringe'][f'ey-{soln}'],
                    params['fringe'][f's1-local-{soln}'],
                    params['fringe']['bc'],
                ),
                (
                    ('s1', 'None', 'None', True),
                    ('ey', 'None', 'None', True),
                    ('s1-local', 'None', 'None', False),
                    ('bc', 'combined', 'sym', False),
                 )
                )
            for x, y in fringe_map:
                for xi, yi in zip(x, y):
                    if xi is None:
                        self.assertTrue(yi is None)
                    else:
                        self.assertEqual(xi, yi)
        
        # params
        attrs = [
            ('d0', )*2,
            ('x0', )*2,
            ('y0', )*2,
            ('w', )*2,
            ('h', )*2,
            ('th', )*2,
            ('Ep', )*2,
            ('nu', )*2,
            ('Fx_bot_brg', )*2,
            ('Fx_bot_byp', )*2,
            ('Fx_lh_brg', )*2,
            ('Fx_lh_byp', )*2,
            ('Fx_rh_brg', )*2, 
            ('Fx_rh_byp', )*2,
            ('Fx_top_brg', )*2,
            ('Fx_top_byp', )*2,
            ('Fy_bot_brg', )*2,
            ('Fy_bot_byp', )*2,
            ('Fy_lh_brg', )*2,
            ('Fy_lh_byp', )*2,
            ('Fy_rh_brg', )*2,
            ('Fy_rh_byp', )*2,
            ('Fy_top_brg', )*2,
            ('Fy_top_byp', )*2,
            ('M_bot_brg', )*2,
            ('M_bot_byp', )*2,
            ('M_lh_brg', )*2,
            ('M_lh_byp', )*2,
            ('M_rh_brg', )*2,
            ('M_rh_byp', )*2,
            ('M_top_brg', )*2,
            ('M_top_byp', )*2,
            ('Px', )*2,
            ('Py', )*2,
            ]
        # print
        for x, y in zip(print_params['params'], attrs):
            sc_name, name = x
            sc_name0, name0 = y 
            self.assertEqual(sc_name, sc_name0)
            self.assertEqual(name, name0)
        # repair
        attrs.remove(('th', )*2)
        attrs.remove(('d0', )*2)
        attrs.extend(
            [('th', 'r_th'),
             ('d0', 'r_d0')])
        for x, y in zip(repair_params['params'], attrs):
            sc_name, name = x
            sc_name0, name0 = y 
            self.assertEqual(sc_name, sc_name0)
            self.assertEqual(name, name0)

    def test_get_sc_results_singlehole(self):
        """
        Test get_sc_results method.
        
        Returns
        -------
        None.

        """
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Configure callback
        self.app.worker_signals = main.WorkerSignals()
        
        # Open StressCheck
        sc, doc, model = self.app.open_sc_model(
            self.app.worker_signals.progress,
            self.app.ctx.single_hole_model
            )
        
        # Set Geometry
        dia = 0.787
        w , h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            w=w,
            h=h,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_neg=858)
        self.setBearingShearLoad(vbs_rh_neg=92135)
        
        # Get solution parameters
        params = self.app._singlehole_soln_params(repair=False)
        
        # Set StressCheck Model Parameters
        self.app.set_model_params(
            doc, 
            self.app.input_tab.coupon, 
            params['params'], 
            self.app.worker_signals.progress
            )
        
        # Add Loads, Contraints, SolutionIDs
        self.app._singlehole_boundary_conditions(
            model,
            params['flags'], 
            )
        
        # Verify SolutionIDs
        solnids = model.SolutionIDs
        current_solnids = {}
        for i in range(solnids.Count):
            soln = solnids.ItemAtIndex(i)
            current_solnids[soln.Name] = (
                soln.ConstraintName,
                soln.LoadName,
                soln.Status,
                )
        solnids = {
            'brg-neg': ('sym', 'brg-neg', 1), 
            'brg-pos': ('sym', 'brg-pos', 1), 
            'byp-neg': ('sym', 'byp-neg', 1), 
            'byp-pos': ('sym', 'byp-pos', 1), 
            'combined': ('sym', 'combined', 1),
            }
        self.assertTrue(
            all([key in solnids.keys() for key in current_solnids.keys()])
            )
        for key, data in current_solnids.items():
            data0 = solnids[key]
            self.assertEqual(len(data), len(data0))
            for x, y in zip(data, data0):
                self.assertEqual(x, y)
        
        # Solve 
        self.app.solve_sc_model(
            sc, 
            params['soln'], 
            self.app.worker_signals.progress,
            )
        
        # Get StressCheck Extractions
        extract = self.app.get_sc_results(doc)
        
        # Close StressCheck
        sc.Close()
        doc, model = None, None
        
        # Open pickled extract
        with open(r'tests\pkl\get_sc_results_loaded.pkl', 'rb') as fp:
            extract0 = pickle.load(fp)
        
        # Verify 
        extract = extract._asdict()
        self.assertTrue(
            all([key in extract0.keys() for key in extract.keys()])
                )
        for key, val in extract.items():
            val0 = extract0[key]
            self.assertEqual(len(val), len(val0))
            for x, y in zip(val, val0):
                self.assertAlmostEqual(x, y, delta=1e-9)
        
        # # Document
        # writer = pd.ExcelWriter(r'tests\xlsx\get_sc_results_loaded.xlsx')
        # data, columns = [], []
        # names = ('byp', 'brg', 's1')
        # for key, val in extract.items():
        #     if any([name in key for name in names]):
        #         val0 = extract0[key]
        #         data.extend([
        #             val, 
        #             val0, 
        #             np.array([abs(x - y) for x, y in zip(val, val0)]),
        #             ])
        #         columns.extend([
        #             f'{key}', 
        #             f'ref-{key}', 
        #             f'{key} delta',
        #             ])
        # df = pd.DataFrame(data=np.array(data).T, columns=columns)
        # df.to_excel(writer, sheet_name='Bypass, Bearing, S1')
        # writer.save()
        # writer.close()

    def test_get_sc_results_satellitehole(self):
        """
        Test get_sc_results method for satellite-hole model.
        
        Returns
        -------
        None.

        """
        def export_pkl(extract, fname):
            """Export extraction to pkl file."""
            extract = extract._asdict()
            with open(fname, 'wb') as fp:
                pickle.dump(extract, fp)
        
        def export_xlsx(extract, pkl_fname):
            """Export extraction comparison to xlsx file."""
            # Open pickled extract
            with open(pkl_fname, 'rb') as fp:
                extract0 = pickle.load(fp)
            
            writer = pd.ExcelWriter(fname.replace('pkl', 'xlsx'))
            data, columns = [], []
            names = ('byp', 'brg', 's1')
            for key, val in extract.items():
                if any([name in key for name in names]):
                    val0 = extract0[key]
                    data.extend([
                        val, 
                        val0, 
                        np.array([abs(x - y) for x, y in zip(val, val0)]),
                        ])
                    columns.extend([
                        f'{key}', 
                        f'ref-{key}', 
                        f'{key} delta',
                        ])
            df = pd.DataFrame(data=np.array(data).T, columns=columns)
            df.to_excel(writer, sheet_name='Results')
            writer.save()
            writer.close()
        
        def verify_extract(extract, pkl_fname):
            """Verify extract to pkled extraction."""
            # Open pickled extract
            with open(pkl_fname, 'rb') as fp:
                extract0 = pickle.load(fp)
            
            # Verify 
            extract = extract._asdict()
            self.assertTrue(
                all([key in extract0.keys() for key in extract.keys()])
                    )
            for key, val in extract.items():
                val0 = extract0[key]
                self.assertEqual(len(val), len(val0))
                for x, y in zip(val, val0):
                    self.assertAlmostEqual(x, y, delta=1e-9)
        
        # Launch Satellite-Hole Model
        sc, doc, model = self.open_model('satellite-hole')
        
        # Set Geometry
        dia = 0.787
        w , h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            x1=w/4,
            y1=h/4,
            d1=dia/4,
            x2=3*w/4,
            y2=3*h/4,
            d2=dia/4,
            w=w,
            h=h,
            th=0.1314,
            Ep=16.0,
            Ef=30.0,
            nf=True,
            csk_depth=0.036
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_neg=858)
        self.setBearingShearLoad(vbs_rh_neg=92135)
        
        # Get solution parameters
        params = self.app._singlehole_soln_params(repair=False)
        
        # Set StressCheck Model Parameters
        self.app.set_model_params(
            doc, 
            self.app.input_tab.coupon, 
            params['params'], 
            self.app.worker_signals.progress
            )
        
        # Add Loads, Contraints, SolutionIDs
        self.app._singlehole_boundary_conditions(
            model,
            params['flags'], 
            )
        
        # Verify SolutionIDs
        solnids = model.SolutionIDs
        current_solnids = {}
        for i in range(solnids.Count):
            soln = solnids.ItemAtIndex(i)
            current_solnids[soln.Name] = (
                soln.ConstraintName,
                soln.LoadName,
                soln.Status,
                )
        solnids = {
            'brg-neg': ('sym', 'brg-neg', 1), 
            'brg-pos': ('sym', 'brg-pos', 1), 
            'byp-neg': ('sym', 'byp-neg', 1), 
            'byp-pos': ('sym', 'byp-pos', 1), 
            'combined': ('sym', 'combined', 1),
            }
        self.assertTrue(
            all([key in solnids.keys() for key in current_solnids.keys()])
            )
        for key, data in current_solnids.items():
            data0 = solnids[key]
            self.assertEqual(len(data), len(data0))
            for x, y in zip(data, data0):
                self.assertEqual(x, y)
        
        # Solve 
        self.app.solve_sc_model(
            sc, 
            params['soln'], 
            self.app.worker_signals.progress,
            )
        
        # Get StressCheck Extractions
        extract = self.app.get_sc_results(doc)
        
        # Close StressCheck
        sc.Close()
        doc, model = None, None
        
        fname = r'tests\pkl\get_sc_results_satellitehole.pkl'
        # Export pkl
        export_pkl(extract, fname=fname)
        
        # Verify
        # verify_extract(extract, pkl_fname=)
        
        # Export Comparison
        export_xlsx(extract, fname)
    
    def test_get_kts(self):
        """
        Test _get_kts method.

        Returns
        -------
        None.

        """
        def verify_kts(extract, repair, fname, document=False):
            """Verify kts values."""
            # Get kts
            kts = self.app._get_kts(
                extract,
                repair=repair, 
                )
            
            # Convert to dict 
            for key in kts.keys():
                kts[key][0] = kts[key][0]._asdict()
            
            # Open Verification dict
            with open(fname, 'rb') as fp:
                kts0 = pickle.load(fp)
            
            # Verify 
            self.assertTrue(
                all(
                    [key in kts0.keys() for key in kts.keys()]
                    )
                )
            for key in kts.keys():
                subdict = kts[key][0]
                for subkey, val in subdict.items():
                    val0 = kts0[key][0][subkey]
                    for x, y in zip(val, val0):
                        self.assertAlmostEqual(x, y, delta=1e-3)
                        # try:
                        #     self.assertAlmostEqual(x, y, delta=1e-3)
                        # except AssertionError:
                        #     print(f'key={key}, subkey={subkey}, {x}, {y}, fname={fname}')
            
            # Document
            if document:
                writer = pd.ExcelWriter(fname.replace('pkl', 'xlsx'))
                for key in kts.keys():
                    data = kts[key][0]
                    df = pd.DataFrame(data=data)
                    df.to_excel(writer, sheet_name=key)
                writer.save()
                writer.close()
        
        # Load pickled results
        with open(r'tests\pkl\get_sc_results_loaded.pkl', 'rb') as fp:
            extract_loaded = pickle.load(fp)
        with open(r'tests\pkl\get_sc_results_open.pkl', 'rb') as fp:
            extract_open = pickle.load(fp)
        
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Set Geometry
        dia = 0.787
        w, h = 8*dia, 4*dia
        self.setPrintGeometry(
            x0=w/2,
            y0=h/2,
            d0=dia,
            w=w,
            h=h,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0.0
            )
        
        # Set Loads
        self.setBypassLoad(fx_byp=619)
        self.setAxialShearLoad(v_bot_neg=760)
        self.setBearingAxialLoad(px_neg=858)
        self.setBearingShearLoad(vbs_rh_neg=92135)
        
        # Convert to namedtuple 
        Extractions = namedtuple('Extractions', extract_loaded.keys())
        extract_loaded = Extractions(**extract_loaded)
        extract_open = Extractions(**extract_open)
        
        repair = False
        # Loaded
        self.assertFalse(self.app.input_tab.print_csk_check.isChecked())
        self.assertFalse(self.app.input_tab.print_neat_check.isChecked())
        verify_kts(extract_loaded, repair, r'tests\pkl\get_kts_loaded.pkl')  # Loaded 
        
        # Loaded, Countersink
        csk_pos = QPoint(2, self.app.input_tab.print_csk_check.height()/2)
        self.clickObject(self.app.input_tab.print_csk_check, pos=csk_pos)
        self.assertTrue(self.app.input_tab.print_csk_check.isChecked())
        self.enterField(self.app.input_tab.print_csk_value, 0.0125)
        self.assertEqual(self.app.input_tab.coupon.csk0, 0.0125)
        verify_kts(extract_loaded, repair, r'tests\pkl\get_kts_loaded_csk.pkl')  # Loaded, csk
        
        # Loaded, Countersink, Neat-Fit
        nf_pos = QPoint(2, self.app.input_tab.print_neat_check.height()/2)
        self.clickObject(self.app.input_tab.print_neat_check, pos=nf_pos)
        self.assertTrue(self.app.input_tab.print_neat_check.isChecked())
        verify_kts(extract_loaded, repair, r'tests\pkl\get_kts_loaded_csk_nf.pkl')  # Loaded, csk, nf
        
        # Loaded, Neat-Fit 
        self.clickObject(self.app.input_tab.print_csk_check, pos=csk_pos)
        self.assertFalse(self.app.input_tab.print_csk_check.isChecked())
        self.assertAlmostEqual(self.app.input_tab.coupon.csk0, 0.0, delta=1e-3)
        verify_kts(extract_loaded, repair, r'tests\pkl\get_kts_loaded_nf.pkl')  # Loaded, nf
        
        # Open
        self.clickObject(self.app.input_tab.print_neat_check, pos=nf_pos)
        self.assertFalse(self.app.input_tab.print_neat_check.isChecked())
        self.setBearingAxialLoad()
        self.setBearingShearLoad()
        verify_kts(extract_open, repair, r'tests\pkl\get_kts_open.pkl')  # Open
        
        # Open, Csk
        self.clickObject(self.app.input_tab.print_csk_check, pos=csk_pos)
        self.assertTrue(self.app.input_tab.print_csk_check.isChecked())
        self.enterField(self.app.input_tab.print_csk_value, 0.0125)
        verify_kts(extract_open, repair, r'tests\pkl\get_kts_open_csk.pkl')  # Open, csk 

    def test_00057114_0(self):
        """
        Test REQ-00057114 holes 8-18 blueprint.

        Returns
        -------
        None.

        """
        # Select Model
        self.clickObject(self.app.singlehole_model, Qt.LeftButton)
        self.assertEqual(self.app.input_tab.objectName(), 'single-hole')
        
        # Set Print Geometry
        self.setPrintGeometry(
            x0=0.492,
            y0=0.9275,
            d0=0.255,
            w=1.5425,
            h=1.855,
            th=0.25,
            Ep=10.3,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # Set Repair Geometry
        self.setRepairGeometry(
            d0=0.3281,
            th=0.235,
            Ef=30.0,
            nf=False,
            csk_depth=0
            )
        
        # Set Loads
        self.setBypassLoad(fy_byp=9809)
        self.setBearingAxialLoad(px_neg=104)
        self.setBearingShearLoad(vbs_rh_neg=1289)
        self.verifyCouponBalance(
            fx_top_brg=-729, 
            fy_top_byp=9809,
            fx_rh_brg=104, 
            fy_rh_brg=-1289,
            fx_bot_brg=729,
            fy_bot_byp=-9809,
            px=-104,
            py=1289
            )
        
        # # Check S1 Gradient
        # pos = QPoint(2, self.app.input_tab.s1_gradient.height()/2)
        # self.clickObject(self.app.input_tab.s1_gradient, pos=pos)
        # self.assertTrue(self.app.input_tab.s1_gradient.isChecked())
        
        # Solve
        self.clickObject(self.app.input_tab.solve_btn)
        self.assertFalse(self.app.input_tab.solve_btn.isEnabled())
        
        # Wait for finished signal
        finished = QSignalSpy(self.app.worker_signals.finished)
        finished.wait(timeout=120000)  # ms
        
        # Check Print KtS, Location, GR, Kc/Kt
        self.verifyCriticalResults(
            self.app.print_results,
            kts=106e3,
            loc='Mid-Plane, 181.0 deg',
            kckt=0.65,
            gr=0.826
            )
        
        # Check Repair KtS, Location, GR, Kc/Kt
        self.verifyCriticalResults(
            self.app.repair_results,
            kts=113e3,
            loc='Mid-Plane, 181.0 deg',
            kckt=0.71,
            gr=0.859
            )
        
        # Open Report Tab 
        self.clickObject(self.app.results_tab.findChild(QPushButton, 'Report Button'))
        
        # Set Platform
        self.setQcomboboxIndex(
            self.app.report_tab.findChild(QComboBox, 'Platform'), 
            'F/A-18E'
            )
        
        # Set Ultimate Load
        sf_widget = self.app.report_tab.findChild(QComboBox, 'EFG Load Type')
        self.setQcomboboxIndex(sf_widget, 'Ultimate')
        self.assertEqual(self.app.get_load_sf(), 1.50)
        
        # Set Print Plate Material Values 
        self.setPlateMaterial(
            matl_type='Aluminum',
            matl_subtype='7050-T74',
            matl_form='Plate',
            matl_grain='L-T',
            matl_stock=4.5,
            repair=False,
            )
        
        # Set Repair Plate Material Values 
        self.setPlateMaterial(
            matl_type='Aluminum',
            matl_subtype='7050-T74',
            matl_form='Plate',
            matl_grain='L-T',
            matl_stock=4.5,
            repair=True,
            )
        
        # Check Print Correction Factors 
        self.verifyCorrectionFactors(
            fsg=1.0,
            fg=0.97,
            ft=0.90,
            fsf=1.0,
            fsc=1.0,
            repair=False
            )
        
        # Check Repair Correction Factors 
        self.verifyCorrectionFactors(
            fsg=0.972,
            fg=0.97,
            ft=0.90,
            fsf=1.0,
            fsc=1.0,
            repair=True
            )
        
        # Interpolate KtDLS 
        self.interpolateKtdls(65, 86, 129)
        self.assertAlmostEqual(
            float(self.app.report_tab.print_ktdls.text()),
            79726.149,
            delta=1e-3
            )
        self.assertAlmostEqual(
            float(self.app.report_tab.repair_ktdls.text()),
            77096.753,
            delta=1e-3
            )
        
        # Check Print Margin
        self.verifyMargin(
            fkts=0.873,
            ktsadj=80630.447, 
            margin=-0.011,
            repair=False)
        
        # Check Repair Margin
        self.verifyMargin(
            fkts=0.849,
            ktsadj=88777.649, 
            margin=-0.132,
            repair=True)
        
        # Save Results
        self.test_file_save_analysis(r'tests/pkl/req-00057014-holes-8-18.pkl')
        self.test_file_save_model(r'tests/scw/req-00057014-holes-8-18')
    
if __name__ == '__main__':
    unittest.main()

