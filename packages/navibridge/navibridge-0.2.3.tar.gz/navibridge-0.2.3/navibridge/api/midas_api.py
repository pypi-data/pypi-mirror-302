import os
import shutil

from .base_api import BaseAPI
from ..zoo import FEM


class MidasAPI(BaseAPI):

    def __init__(self, project, root_path, init=True):
        super().__init__(project, root_path, init)
        self.options = {}
        self.fem: 'FEM' = None
        self.project_name = project
        wdr = os.path.join(root_path, self.project_name)
        self.cwd = os.path.abspath(wdr)
        self.res_dir = os.path.join(os.path.abspath(root_path), f'{project}_result.txt')
        self.init = init
        if init:
            if not os.path.exists(wdr):
                os.mkdir(wdr)
            else:
                shutil.rmtree(wdr)
                os.mkdir(wdr)

    def run_fem(self, fem_model: FEM):
        self.fem = fem_model
        file_out = open(os.path.join(self.cwd, self.project_name + '.mct'), 'w+', encoding='GBK')
        self._begin(file_out)
        self._temp(file_out)
        self._sections(file_out)
        self._nodes(file_out)
        self._elems(file_out)
        self._constraint(file_out)
        self.to_mct_rq(file_out, self.loads['rq'])
        self.to_mct_dead2(file_out, self.loads['dw'], self.loads['snow'])
        self.to_mct_wind(file_out, 20, 40, 0.785, 0.22, 1.26, 0.87, 40, truss_height_m=3.0)
        file_out.close()

    def _begin(self, fid):
        fid.write("*UNIT\n")
        fid.write("N, mm, KJ, C\n")
        fid.write("*STRUCTYPE\n")
        fid.write("0,1,1,NO,YES,9806,0,NO,NO,NO\n")
        if len(self.fem.mat_list) != 0:
            fid.write("*MATERIAL \n")
            for ky in self.fem.mat_list.keys():
                m = self.fem.mat_list[ky]
                fid.write(m.mct_str)
                fid.write('\n')
        fid.write("*STLDCASE\n")
        fid.write("; LCNAME, LCTYPE, DESC\n")
        fid.write("   自重 , USER, \n")
        fid.write("   二期 , USER, \n")
        fid.write("   W1主梁横风, USER, \n")
        fid.write("   W1立柱横风, USER, \n")
        fid.write("   W1立柱纵风, USER, \n")
        fid.write("   W2主梁横风, USER, \n")
        fid.write("   W2立柱横风, USER, \n")
        fid.write("   W2立柱纵风, USER, \n")
        fid.write("   整体升温, USER, \n")
        fid.write("   整体降温, USER, \n")
        fid.write("   雪荷载, USER, \n")
        fid.write("*USE-STLD, 自重\n")
        fid.write("*SELFWEIGHT\n")
        fid.write("0, 0, -1,\n")

    def _temp(self, fid):
        fid.write("*USE-STLD, 整体升温\n")
        fid.write("*SYSTEMPER\n")
        fid.write(f"{self.loads['temp_up']}, \n")
        fid.write("*USE-STLD, 整体降温\n")
        fid.write("*SYSTEMPER\n")
        fid.write(f"{self.loads['temp_down']}, \n")

    def _sections(self, fid):
        fid.write("*SECTION\n")
        for ky in self.fem.sect_list.keys():
            s = self.fem.sect_list[ky]
            if hasattr(s, 'mct_str'):
                fid.write(s.mct_str)

    def _nodes(self, fid):
        fid.write("*NODE\n")
        for n in self.fem.node_list.keys():
            nd = self.fem.node_list[n]
            fid.write("%i,%.6f,%.6f,%.6f\n" % (nd.id, nd.x, nd.y, nd.z))

    def _elems(self, fid):
        fid.write("*ELEMENT\n")
        for ky in self.fem.elem_list.keys():
            e = self.fem.elem_list[ky]
            n1 = e.nlist[0].id
            n2 = e.nlist[1].id
            iMat = e.mat
            iSecn = e.secn
            beta = 90 if (iSecn == 15 or iSecn == 17) else 0
            fid.write(" %i,BEAM,%i,%i,%i,%i,%i,0\n" % (e.id, iMat, iSecn, n1, n2, beta))

    def _constraint(self, fid):
        fid.write("*CONSTRAINT    ; Supports\n")
        for ky in self.fem.fix_list.keys():
            f = self.fem.fix_list[ky]
            if hasattr(f, 'mct_str'):
                fid.write(f.mct_str)

    def to_mct_dead2(self, fid, dw2, snow):
        e2dead2 = [e for e in self.fem.top_elem_list.keys() if e // 1000 == 51 or e // 1000 == 53]
        e2dead2.sort()
        if len(e2dead2) != 0:
            fid.write("*USE-STLD,二期\n")
            fid.write("*BEAMLOAD \n")
        for ee in e2dead2:
            fid.write(
                " %i, BEAM   , UNILOAD, GZ, NO , NO, aDir[1], , , , 0, %.3f, 1, %.3f, 0, 0, 0, 0, , NO, 0, 0, NO, \n" % (
                    ee, -dw2 * 0.5, -dw2 * 0.5))
        fid.write("*USE-STLD,雪荷载\n")
        fid.write("*BEAMLOAD \n")
        for ee in e2dead2:
            fid.write(
                " %i, BEAM   , UNILOAD, GZ, NO , NO, aDir[1], , , , 0, %.3f, 1, %.3f, 0, 0, 0, 0, , NO, 0, 0, NO, \n" % (
                    ee, -snow * 0.5, -snow * 0.5))

    def to_mct_rq(self, fid, rq):
        fid.write("*MVLDCODE\n")
        fid.write("   CODE=CHINA\n")
        fid.write("*LINELANE(CH) \n")
        fid.write("   NAME=L, LANE, , 0, 0, BOTH, 500, 3000, NO, 3000\n")
        e2rq = [e for e in self.fem.top_elem_list.keys() if e // 1000 == 53]
        e2rq.sort()
        for ii, e in enumerate(e2rq):
            if ii == 0:
                st = "YES"
                ed = ", "
            elif ii != len(e2rq) - 1:
                st = "NO"
                if ii % 2 != 0:
                    ed = '\n'
                else:
                    ed = ", "
            else:
                st = "NO"
                ed = '\n'
            fid.write("     %i, %f, 120000, %s ,1 %s" % (e, 2250, st, ed))
        fid.write("*VEHICLE\n")
        fid.write(f"   NAME=专用人行荷载, 2, CROWD, 1, {rq}\n")
        fid.write("*MVLDCASE(CH)   \n")
        fid.write("   NAME=RQ, , NO, 2, 1, 0\n")
        fid.write("        1, 1, 0.8, 0.67, 0.6, 0.55, 0.55, 0.55\n")
        fid.write("        1, 1, 0.78, 0.67, 0.6, 0.55, 0.52, 0.5\n")
        fid.write("        1.2, 1, 0.78, 0.67, 0.6, 0.55, 0.52, 0.5\n")
        fid.write("        VL, 专用人行荷载, 1, 0, 1, L\n")
        fid.write("*MOVE-CTRL(CH) \n")
        fid.write("   INF, 0, 3, NODAL, NO, AXIAL, YES,   YES, NO, ,   YES, NO, ,   YES, NO, ,   YES, NO,   , NO, 0, 0, YES, 0\n")
        fid.write("   0\n")

    # def to_mct_wind(self, fid, U10W1, U10W2, kc, alpha0, gv, CY, func_D):
    def to_mct_wind(self, fid, U10W1, U10W2, kc, alpha0, gv, CY, truss_z0_m, truss_height_m):
        zz0 = truss_z0_m
        UdW1 = self.GetUd(U10W1, zz0, kc, 1, alpha0).m
        FgW1 = self.getFg(gv, UdW1, CY, truss_height_m).m * 1e-3  # N/mm
        UdW2 = self.GetUd(U10W2, zz0, kc, 1, alpha0).m
        FgW2 = self.getFg(gv, UdW2, CY, truss_height_m).m * 1e-3  # N/mm

        e2windy_beam = [e for e in self.fem.left_elem_list.keys() if e < 1e5]  # or e // 1000 == 54]
        fid.write("*USE-STLD,W1主梁横风\n")
        fid.write("*BEAMLOAD \n")
        for ee in e2windy_beam:
            fid.write(
                " %i, BEAM , UNILOAD, GY, NO , NO, aDir[1], , , , 0, %.3f, 1, %.3f, 0, 0, 0, 0, , NO, 0, 0, NO, \n" % (
                    ee, -FgW1 * 0.5, -FgW1 * 0.5))
        fid.write("*USE-STLD,W2主梁横风\n")
        fid.write("*BEAMLOAD \n")
        for ee in e2windy_beam:
            fid.write(
                " %i, BEAM , UNILOAD, GY, NO , NO, aDir[1], , , , 0, %.3f, 1, %.3f, 0, 0, 0, 0, , NO, 0, 0, NO, \n" % (
                    ee, -FgW2 * 0.5, -FgW2 * 0.5))
        e2windx_tower = [e for e in self.fem.left_elem_list.keys() if e > 1e5]
        fid.write("*USE-STLD,W1立柱横风\n")
        fid.write("*BEAMLOAD \n")
        for ee in e2windx_tower:
            ele = self.fem.elem_list[ee]
            z0 = ele.location[0] * 1e-3 * self.options['slope'] - self.options['truss_h'] * 1e-3
            dist = z0 - ele.location[2] * 1e-3
            zi = zz0 - dist
            dx = self.options['k_l'] * dist
            D = self.options['truss_l'] * 1e-3 + 2 * dx
            zi = max(zi, 0.1)
            UdW1 = self.GetUd(U10W1, zi, kc, 1, alpha0).m
            FgW1 = self.getFg(gv, UdW1, CY, D).m * 1e-3  # N/mm
            fid.write(
                " %i, BEAM , UNILOAD, GY, NO , NO, aDir[1], , , , 0, %.3f, 1, %.3f, 0, 0, 0, 0, , NO, 0, 0, NO, \n" % (
                    ee, -FgW1 * 0.5, -FgW1 * 0.5))
        fid.write("*USE-STLD,W2立柱横风\n")
        fid.write("*BEAMLOAD \n")
        for ee in e2windx_tower:
            ele = self.fem.elem_list[ee]
            z0 = ele.location[0] * 1e-3 * self.options['slope'] - self.options['truss_h'] * 1e-3
            dist = z0 - ele.location[2] * 1e-3
            zi = zz0 - dist
            dx = self.options['k_l'] * dist
            D = self.options['truss_l'] * 1e-3 + 2 * dx
            zi = max(zi, 0.1)
            UdW2 = self.GetUd(U10W2, zi, kc, 1, alpha0).m
            FgW2 = self.getFg(gv, UdW2, CY, D).m * 1e-3  # N/mm
            fid.write(
                " %i, BEAM , UNILOAD, GY, NO , NO, aDir[1], , , , 0, %.3f, 1, %.3f, 0, 0, 0, 0, , NO, 0, 0, NO, \n" % (
                    ee, -FgW2 * 0.5, -FgW2 * 0.5))
        return

    def clear(self):
        if self.init:
            shutil.rmtree(self.cwd)
        pass
