#!/usr/bin/env python
#
# Hi There!
# You may be wondering what this giant blob of binary data here is, you might
# even be worried that we're up to something nefarious (good for you for being
# paranoid!). This is a base85 encoding of a zip file, this zip file contains
# an entire copy of pip (version 20.0.2).
#
# Pip is a thing that installs packages, pip itself is a package that someone
# might want to install, especially if they're looking to run this get-pip.py
# script. Pip has a lot of code to deal with the security of installing
# packages, various edge cases on various platforms, and other such sort of
# "tribal knowledge" that has been encoded in its code base. Because of this
# we basically include an entire copy of pip inside this blob. We do this
# because the alternatives are attempt to implement a "minipip" that probably
# doesn't do things correctly and has weird edge cases, or compress pip itself
# down into a single file.
#
# If you're wondering how this is created, it is using an invoke task located
# in tasks/generate.py called "installer". It can be invoked by using
# ``invoke generate.installer``.

import os.path
import pkgutil
import shutil
import sys
import struct
import tempfile

# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    iterbytes = iter
else:
    def iterbytes(buf):
        return (ord(byte) for byte in buf)

try:
    from base64 import b85decode
except ImportError:
    _b85alphabet = (b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    b"abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~")

    def b85decode(b):
        _b85dec = [None] * 256
        for i, c in enumerate(iterbytes(_b85alphabet)):
            _b85dec[c] = i

        padding = (-len(b)) % 5
        b = b + b'~' * padding
        out = []
        packI = struct.Struct('!I').pack
        for i in range(0, len(b), 5):
            chunk = b[i:i + 5]
            acc = 0
            try:
                for c in iterbytes(chunk):
                    acc = acc * 85 + _b85dec[c]
            except TypeError:
                for j, c in enumerate(iterbytes(chunk)):
                    if _b85dec[c] is None:
                        raise ValueError(
                            'bad base85 character at position %d' % (i + j)
                        )
                raise
            try:
                out.append(packI(acc))
            except struct.error:
                raise ValueError('base85 overflow in hunk starting at byte %d'
                                 % i)

        result = b''.join(out)
        if padding:
            result = result[:-padding]
        return result


def bootstrap(tmpdir=None):
    # Import pip so we can use it to install pip and maybe setuptools too
    from pip._internal.cli.main import main as pip_entry_point
    from pip._internal.commands.install import InstallCommand
    from pip._internal.req.constructors import install_req_from_line

    # Wrapper to provide default certificate with the lowest priority
    # Due to pip._internal.commands.commands_dict structure, a monkeypatch
    # seems the simplest workaround.
    install_parse_args = InstallCommand.parse_args
    def cert_parse_args(self, args):
        # If cert isn't specified in config or environment, we provide our
        # own certificate through defaults.
        # This allows user to specify custom cert anywhere one likes:
        # config, environment variable or argv.
        if not self.parser.get_default_values().cert:
            self.parser.defaults["cert"] = cert_path  # calculated below
        return install_parse_args(self, args)
    InstallCommand.parse_args = cert_parse_args

    implicit_pip = True
    implicit_setuptools = True
    implicit_wheel = True

    # Check if the user has requested us not to install setuptools
    if "--no-setuptools" in sys.argv or os.environ.get("PIP_NO_SETUPTOOLS"):
        args = [x for x in sys.argv[1:] if x != "--no-setuptools"]
        implicit_setuptools = False
    else:
        args = sys.argv[1:]

    # Check if the user has requested us not to install wheel
    if "--no-wheel" in args or os.environ.get("PIP_NO_WHEEL"):
        args = [x for x in args if x != "--no-wheel"]
        implicit_wheel = False

    # We only want to implicitly install setuptools and wheel if they don't
    # already exist on the target platform.
    if implicit_setuptools:
        try:
            import setuptools  # noqa
            implicit_setuptools = False
        except ImportError:
            pass
    if implicit_wheel:
        try:
            import wheel  # noqa
            implicit_wheel = False
        except ImportError:
            pass

    # We want to support people passing things like 'pip<8' to get-pip.py which
    # will let them install a specific version. However because of the dreaded
    # DoubleRequirement error if any of the args look like they might be a
    # specific for one of our packages, then we'll turn off the implicit
    # install of them.
    for arg in args:
        try:
            req = install_req_from_line(arg)
        except Exception:
            continue

        if implicit_pip and req.name == "pip":
            implicit_pip = False
        elif implicit_setuptools and req.name == "setuptools":
            implicit_setuptools = False
        elif implicit_wheel and req.name == "wheel":
            implicit_wheel = False

    # Add any implicit installations to the end of our args
    if implicit_pip:
        args += ["pip"]
    if implicit_setuptools:
        args += ["setuptools"]
    if implicit_wheel:
        args += ["wheel"]

    # Add our default arguments
    args = ["install", "--upgrade", "--force-reinstall"] + args

    delete_tmpdir = False
    try:
        # Create a temporary directory to act as a working directory if we were
        # not given one.
        if tmpdir is None:
            tmpdir = tempfile.mkdtemp()
            delete_tmpdir = True

        # We need to extract the SSL certificates from requests so that they
        # can be passed to --cert
        cert_path = os.path.join(tmpdir, "cacert.pem")
        with open(cert_path, "wb") as cert:
            cert.write(pkgutil.get_data("pip._vendor.certifi", "cacert.pem"))

        # Execute the included pip and use it to install the latest pip and
        # setuptools from PyPI
        sys.exit(pip_entry_point(args))
    finally:
        # Remove our temporary directory
        if delete_tmpdir and tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    tmpdir = None
    try:
        # Create a temporary working directory
        tmpdir = tempfile.mkdtemp()

        # Unpack the zipfile into the temporary directory
        pip_zip = os.path.join(tmpdir, "pip.zip")
        with open(pip_zip, "wb") as fp:
            fp.write(b85decode(DATA.replace(b"\n", b"")))

        # Add the zipfile to sys.path so that we can import it
        sys.path.insert(0, pip_zip)

        # Run the bootstrap
        bootstrap(tmpdir=tmpdir)
    finally:
        # Clean up our temporary working directory
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


DATA = b"""
P)h>@6aWAK2mt$aI8cj~)bS$$0074U000jF003}la4%n9X>MtBUtcb8d2NtyYr-%Phu`N@9Nmj4xKw1
YO>i(|e`H&gvAqzH5bae1Z4z?VNx%J4r5gi7-sG3#xx1$bt^#koRK_v}t4mq4DM@nUjopE%ybBEP%f(
VnUmmBg>f<ZRX4$h4rZ^Li1;kUd)c=GxLp*@FXX9cMA%s%j7%0A!f(ay}p&ZIl5<hY*pwh<nblA}(a~
At2>P3shG4wjhs)eqI!+PC^t9ytm91D{q`P>_Vc(sLYF?d+az}d2a3bkb@T!5MoHcczwlE57-Y@H=nB
G5J%&m_eW_!LWZo|{u!$dPq)Gyp<`J+r5An(hqm>y6yHD)o)mX=J8`s76X}uJ3MTH`$+{bK22zXuOLl
b>`F|XzwwcMhVDuu)pC^QeXT4P)h>@6aWAK2mn=HCQw^Dq9IEG004Lb000jF003}la4%n9ZDDC{Utcb
8d0kO4Zo@DP-1Q0q8SE6P(>Xwfj$MoHf@(`KQCU(&8g71HO0ki&o+$e6NZz>|C(zo>JZGyl;FMx!FrO
6t%vRstO0E4!TSZq=Y6ou)77Hd@$a4r7F5rryfn~JTAHWO)@Mv#O;8=KFGCT_RV?+YueO#zwW-=EG>B
?gakT5+zb<60FQUL~HLEgIxovfWq|0NvR`+SC`IVq5DSMEVyuc5y>N3AD=LF+DESFFQK3<Kt1CJTKTL
Yy%XL<h|yp*aBAK8E2AC<u{lR;_nSv*%($xv)$xXH{VlyW4<F*1MJTS{*X{Xbw;;w)Q4$fyk7KuYb>y
L&bIL-tGVQ=D>bmS(|PrKHALf%b^PGm8xlpc&9P26|(Pok6k%>8(nKdP@O0nBT4&2Uy{oXLi{%BmPVP
pMzPtpMpEY6ALO>STiNOtP)h>@6aWAK2mn=HCQ$9^SDrcn000F7000>P003}la4%nJZggdGZeeUMUte
i%X>?y-E^v8mkxxqlF%ZS?`4nS&u~0V`K`rP-{D)da^iYZ{>F#WIWH*U3v&w#Z<JKxdLk?k>_vXzn<2
~C6+ZB0>{sUsKb?}DT7+4`v%yROI>|K*}N{wXX->}eJu;>_-otL2%#^A%dGZlw+r%wAwehoj)_lw6xe
tvy%ew#nN%;z`rD`TkIQJxt{XK?-R@DP<kvY)~oi5g={te|z|_Z_e0bRIlTHsbNO5@)c#l`Ov%OHqD(
oxs5vq@+XRXf%4RNg&<GD99gJLKPT7Q$i8Ega$zhrl<m1J5BR?khER{D+I<08GVsL4tAuO86KC(!j&a
$rbCJ95|JqgBGjr;X4bAr>u!}5p|!D(&L)JGL^>3Eba--{Z3F({*aaEAavwvg%9d09$u36ZO_cOy9sA
$nz-nT?08mQ<1QY-O00;o2WSLLXN3s5L2><|W9RL6t0001RX>c!JX>N37a&BR4FJg6RY-C?$Zgwtkd7
T+uZ`-={-M@lM9wcFsu<p^A2i)7Hx5c_7XwwaaVF-#uC%lnGj+BykMgIHF;fF*@a@sq;*rLw&H;>QG&
VKD#Q<IDKkxAYjXxouq(VFbJBuw$9>=<uJ-AmTq5mhtQkz2%o$JN={*=lu8Ztf|7Hw}M6n2H}X6?M;h
Abd-SqzC>8BuhBt2TBBI@Se4#L&U!8CC!1%;V6!4qB_Z{F5?3Emd)mU*(f@^1^y*6%KElD3R-71-75>
TVh6!xM;d;2htk<cuG}wm9Da86xqFhOSnVZ0fXGclD`cpM1-Ozmm9%~bvKScDyzf|}av)RjcF*n{>>c
e2aqRASTQuy}fG-1;-Mv~F0Kr6FJkqx2G8Yebg`|r2vZ8|opXq;k2BrgBrsQ8#DiH52kZeGtl>D2^2T
<}0?M8YIvnckgp+!MTg~vt1EA2&(F*txqFmG;E>TiYQz<l6dftic(_%v!q52C1<bci?b{0`)<Ixdf|p
dAGUi$(h9x9e}k+Yc9S|51GYdU^Tr^0(8NJ#$!G(6&%Or==3Szh5A;UJ>|cS|P`qUNkf%V84`n1p4JI
K3>_VOUWm2_lO(H!P=TW=c240$~y|ShQ~quYjgTuAFfsyi|}&ef-;9N_@vL`qG-zlcqv(}R#j7i>5FS
g_w0GS(u^Up!IP|IT~Wk}Hv5!d{3J#t{G6jsbWLK&nS^A2CzrgX!&^kj5d*m6SNKBFt{3peq)zbambK
cUn=xkN0Rlf!+eHM-%~g&nkj=&%Q6NPk!4-QhgjOX=1H{Kts?GQ4wp27)YoStrhZ5tRybKu0Hd2*jqE
pe%)A^Ejpfl13!wy*)c^TJnlpL#zhX$D`OL^2h6x1PdeY`$Gg@fdm7_H5bs9vBCX`K&v0%{XrI$I1$9
;4I{d$eMER+$2n5~K7+yJ;i=kUv4<M)s#DfT;&LHjdspu&j0*oTB3tu-aOL(QxRTpTkKVi`@{Jx<_~|
BIdWhgUxI#LK}E1Y1u*TD%+YI$`&#Jf7=EErJs831>D10)j@$VodhCXC`af->@P+AiI6XbinIxfQ49s
M-kfQk83=TitR|So`V@`f)&Dq*{upCEb;%k-5}>#8-=V3+p#ZswaD-2iBp`y_Rp$<L!8mHUJd{lY$pC
#)HsvuIp_7@EHb1q?cB4J8Vr`)k>?Yv8hhGIpnT!QcDoH^U7zE-50OQa;`D5AiRK=jxLP!k)=B0oNUB
?E^)s<uc!^xOKTlO&Av1fvF^0rqUKd}E&qF6^En*7knAkq|sG06oKK5T;!hwunF$HAQeq(BuR9?MEMJ
_t)FA>cbh*OqrRT2sF)@Fm*vd!UAk0`z1B#Vkg!M4MDoLpKKq`1x^3Nzy-tghgb6Gn)Hl5*R3$&66Jo
afHxOP?K8T4T$s^qC~|Z;Yn}+?BM~9r%(gX69b=NQ(sCd2W~~FTomL2vIP#Gq6Fuiy$G4^MgAlKK6Vp
dUeg*Y*vzm|6wS_t5i-?oO!WvkgE}YgAxL46s3jLRPBIfGP*8RK(_JT@VRFe}Dkx#nI;z6<YWS&@->!
Ev_=lE1wWcK_B<<p42BXs$NkPng_k;FN@?|}P#t**D%euyI^pEkl$7|#Lo-?#Oe5n@M%yJ~`a;J0{?9
pIgObwPSSZPjk$<EtF&ibX#eulb;W~QM9^>mgPEe0daD9lxGN@H%$1Xu{bFBE2<IwjymoOEC=GEI-sg
{V6>MG~jsp-k#3X@`A(0CJxos$5+@8Bs7ZP{<q9ed@-aj=;GWrx}{$du*K0oxCXD_zx*@qHe-Q<GQLD
G$>B?^GU-Np7N0b#N({yWB*>G+wE|Jv%MV-a4LDN;a~r9^8wra^|zZ3SC^MpU%y;@{_^qWVm#9je(fI
TNn0j@R_hlF-qb|^<TThCz9S??tpyJKXluIe#SS7@qG6pY&58<tGBF*=WmZ_RcO#f*tX|Ym8RO8TM!+
>0nV1%!;~|}ZPHnd)(VJ)y=oHmKXpi<w7#Yvr^@~1N1rAT<*CSpN_0g>tGw5fy=9n-*)9F!3CqUqf9E
@{-2`aR^b%@1LI*#TU=2=m25fAL<Q8yp@L;S79-C><^j7R;ehL&wF{_hDqcLY3}R`;}eDCD@@P}aI|q
?VYt+qoWAHAj7S-@?^>Ykt9t6!%8Eoxad(z%j_-Qt=rsyRs#J#onYsdt{`tI~6R4zF2F7CVWp~dt0GU
U!O`S6?LM8B^`2C6LJTp)Jal^<_k9bc39J<?h7}4#|*ttpC@d=<8mmTl)YI^0t#l@pAy1PCy&eZ9aul
995)}ax2A&Zf*V5&w36g>^iEX9vaeBQfRI~Mbko%r4tXc2ddAXJaW4`>Uy*le`<Go_DnIPt@-iQ;7e5
}AH#`3#Crwy+Y*VMz81FWC!iW#@Wfa4#lF~8w!)?;YcO>Nj2Z=IPW_^_^KzZD(qKE?m9E<@7eIGcDFW
o9^q_&itd7jUUfW1U+Cb#PCRFqLje_k+GKfRxtP#l(4c+HvKM1p(^9BbS(@&ZTB#y^}+=ri0ZI<p9L!
yF_H*2maiqvCDDdUe`vvW(r~MKc>p26pr;YkAg#hUUSo#++7q+@8__j3=ngnc0A4j<?6~)w?_x#jGB2
D7o10al8FUKf#5!fvWwtaUc2a;@7Xgh4w-NxvP7WJ$h3J77R0T6%h2D<c-^3;2=`Uqh4XO&Cxwh+MB^
uW))U;kXI(+^N?sdVUo<nv$F}vmqp~y6Zl+GxE5D5jtXt@=(S9b(#T#j_3AHnGJ>k#qjifVEP6>2f7s
Fc-=dcdYGO4Q&wL+@rwb;wI&7niftVvG)T-UQPy@6q3k`)v_rTw*ck_BU;gD(cOk-t$6{S8wkKKG?2*
UvbQ{zm+qG9a=%H<piUj?4Mu6TxUnTCr}O=IWT8R_10)p>L~3HN?l7kK;w(iSvBP#}(9yP$bmlKTIo0
!uXHBiz?1+})N)k0t;(Py5Ns=^HDNU!E2=9`0|9*w$ga%dlsmER#QGVq}s!(2e~b|5Lc+S7NrkogR#P
++U!UW?bk^MyBTiok@Cci|&|WI=mmRZ3Rg46L+o|*dHChLjorz*br#3MH`N;BZn>56z<eDO^>iFnWFd
?#m588h6qmU3n{sTx$S>YO9KQH000080Cqb!P(t>^^w<jk097pj02TlM0B~t=FJEbHbY*gGVQepBVPj
}zE^vA6T3e6X#ua|oub9#grV1`MU8F85Q~^@QPK-KE5pQ4wiv=+vN7C37$#TeDD@Oi%zjKC{;YGWfIB
5_xde{|*bIzRmZRC00QyK4-_*!Oirw%Hs7M|xV7LUXwR=0VY=C?ZAi8w#dOJVkTohD+VM5zw>jY@>XV
t!Df$Ti;UOjHC|S9PgEpgA0i<4TyS)Nyr|7nRO4nXaG9)TqTmABw!J#9o?xsyFT9Ta#z)_cY(_aDMxk
o5f;V<_A&eB8+ZSmgHqv$oQS4U1246Ml@SNjVg;$;ct}5g9-*KH>xxs<t}7(rPB^uEVDe*u}t+3iqW}
rFk-M3s`s&C7CX2X*$rTlH+!Yh=Q>pkIs<vg6P21U)!Dli^d-LEvGtZvwtE@>+-7DXtkj{15?!|2FY)
|^E>&FR<?#-%V?nxafWH3z-`_`1zk2rcU(vVUy?XWH)t9Fs>#`SJA*+2<<q_7P@$C$r)k5II$c9IL)7
VQOUaKmAL=66Zo*e`61<YyDgWYcqmvT4WKbGh=FAuVc;ykO$yc6wnUVUm87Yi~-Rf=_Mnc+@VFL}+6*
f64KxmYX`wG|QBHN+lQezLSYJ|YIyO87+o6}%!K*SKDav(M-Y?}7h)tKdGFkXVzORKe@y#l@#0-(rdI
kx<HGNS;a%2IP>_gh_oUjGq80D39K$qgh{;HB8^ALY5NRHf!Gtyg+y>Zy5-c8MtXAO{_KVTr$4W9^bf
SXixV|sInN6@;%<~Etlb5y-)N`naU@g<5U_WIG*_V<}IwN;Tm*)4sJH!P{!~j-ghR7GQZJ@GH@;mK}l
nf8Y@tRNMt3gw#X~s_>7A_D`Mtg!N{yv9IVPbuSi4`fB0261{f-M1xpf^P68X~xuLPjarQx19U}T{G=
xt?ZWNhnsbtdF?#Y8Cg;AA6mH@L7w|gD$8+r_#zC~;>J%%>U8py*zM<4$&6L5SiWR{4>Ca=p_;h|Ivo
@eQ?Jx?I^)XFSdC0GfvX~Ot*6-B;L={D#k8H{8Uj7e`aI<RFn<AM0tU#~jLewAmc12c62UtudDyG*ys
u%l+#?Sk|boG;6(o;U%c$W2J`B-94x<ae)nK*AXIAnPIckP_NDa{Bd10K?5AVPN-YrMJ<D<G!==gJ)G
m&Sy2~{WxZK?vSv~;O_nq-%_mCqaz&UA|yqYZH~RL!OBFb+R6CXD4aZMPL-5%SY;GyS%KXi*w2@WqIq
d8mcGE^kp2&~si-1ob@LXL0F3WeSNmT2y<}c8A&s3QMhPF$So}j=e6nP}N2vicdZSZa9W9nTO%QV#!h
|kG3x|a_O5946AaL59$`rz#f{O^G9a^dlo<MkA_9qA87GWpP9#<`-gYGSHRjM-rB**&h+m~Q6mh`N_w
BGHha=8KDc#YJGBx}0*r<6M`rh0tjt=(}kxvSjdHHk1cj*EjVt1y_%6{(4GX+%=M=BUNns|5*_cX6(v
{3Ensw;@yKL%Y}Ro7EtubccqrD3C>cZ|$)f{i`AJpvQK-Tn>mPIj@EHr~&LyE?pfx;|#)DAk7mDE7+z
O(#PX86;|Zhxbnu4!XOr>vUKnn71t%1333U-N=0EA$|iJweG-Tb<jeRa1=JGh9&am|f`F>PJ0J3KonT
)ZfjDd|UbPIxS8&A}0^<a=-Kr8v5QkVb9^^a77^MJZ5C>7elP#LqB{pJ-Kd==?-6To)%6gn^8;Q0lcb
scytv<uchR{Bfa&3;6sC#dyfQQ9W){<DuI9uk0gDu6TbO3)#^pfFPgD>lhgh!C3-VAmEA06gkd;Yp-w
6kf;@zv_$I%v4Rx>$YMKYY4+(my;|U0?UyHgyT3x+mQIc5&|iCOUoaK)kmSCxg_FzfzDI#iVO0#@m(2
k+9O%NRJ(5rx1JYZm&Z;i^Em!i!4rS#5JeG6gFHQ<XZ#);_#p|d~5nn(nP0d*F1Bizd~7?(rJ3OQKUo
^f(Z=OSUcR*8l|D^qD&>Y7j)x~q9{&&o?DF<N2n(2PRA1JAp>_R!r~}&SId%jXTiuWtWnrVGzx^w#~@
!*&lNfd_ElAw)%p1j9Mzi;o6n15A<vQX&$TfqPtX5$@%JZF3%l~h9Xu;!yy!3Q18ta|KsW3D9|`I~3C
iha=X3iXnW)J`@I3Uc%FRJRKR}A?e8NtVPUWVc8-4U$6sM}svtysCfHOj@w8;+~`Gc@VQFPP|<>h3@J
Y91;iH~k^=?2;X9mCk#2<pm_UEdPTG+;DNiAEjJkga)w=LzdXFz%^14#0;<#{RUmJwbV|S~8z&$D-iD
4Ld|Xmm$C!k;r_mL0qc(9u_+B>Feld?t<F0D8%M888p?2?L*Sq65j8Y0w&NY*B^<?Z@&1ZncxcB7+NO
MJbzagbR^>QXX}f<bTD>TbSJBAk9iNr4yvEP_-Uy7`FCNLV<+xGdrv;e+5^kVc9zG-NR6oaDz9D~ij+
s}DtT6xdD&*3*#m#hN$%vZD_A()&=|=U97$galC-(L8Pu#lmF(U-nd07HIE*=;miCu!9C3X(aCZ&jpF
2FFp)5R^>Wsieir{!DcXsQX#KJIa!l-k6Cow}=l7{b)mUJaW=8NpE-c$V**lPNgBvUqUSa7&8MkOCB)
Hqc#s|&V(IZmcCH9EH&z`oXmn{Nc{ESCQ|qu8eMMB?PS(N0_KjSbAgp!`Ui67FZs3?DWkJT({`Q$Lvz
j*`L2!R3ePl<h8m`v?bb3knX3cMji%fw74{Zae7@6Lugxt0FHDe|9Ub|8dB0?1Za;4*Z`@{abNuMs4H
Q?q-=C1$B7by>LI<%>3QcI%L%Ruw?=p{4NW)`@jSB7@4WlrVsDwyrp-Pv#5})`|{DE*=uC_p4K<ba2z
JCxTOaW#X%g~&)qfO9~^D#T%=%5(*;a>UD)Ev>ca+0bkSmI>U(F{pG2=m39LuUHGXqqv%l;upURXv)B
mYeD4vD8P=x1ATyz`xB>zEWJd$Xgl#a9oymLiCGHW};w%-HHC*dcEfb<e9f?C>A@#aRy(khNyoWAEkC
WT<p9FT;GA4Aoly?dlGz7d$Pvu$pIHVVrsLGVn%$(;?EkG-zpXxm)ZuzfHi_F{y4t6TKHt@zla=0ocJ
-q*OD;}NgfxEn(y-86#{zCxOgaz5Tsf7eNJT=tGDY?r**8hRKrPIMgW=^eX2XqDUs!s@OOi2csj+u6V
jx<+h3)Ls2ppDKooRONA6b6PK0+sk*qr)W9YX@3(i`$K@4G8WN8XSEu<upQP&G<;mh$B93!Pp~sRz+P
X6iQ3dVfAW?--iuv^Hky9(;RJv2;YXG`{=vmj5P9>!Nv`bt4!M{eSwR2=!Zi?)lb3o^lg;vY4A?@iX#
nSm>BQ{ZJ_KS`WA0};S)Hz&5;YNTh1>a&KlG@X_T!QGC&yDxdd^_Z&fU&s8Sl?k6+euKX)iN@o0ryrY
}8AMdLJDqRt?DyP6Jyp-|?Pe-95rxP69;F&;!Cl6r6DGHH}dFuFgyfDGFM?^J^1-5U_jt9sJ8>|HFl6
1<DSmY#vvlZUsGlXOntdDvpx6dW<}Mi=3k9HzX)RM?Y~m-dkPYUsB&!O>-RVe)zK<{^rL=#gwc)MJ%7
OIL??t&rzPO$464RyBr@L%EBMBGFOcM^oD12P>Y~f=IQq5O(~0svbhkND3xnNDX8{A4ajSj=u4_k8bF
#X*=l!J%2;jd6g6g|@Bk}CqzjzliRIk{RF?Om@hmF8V^pP5TX$%0LAH5K6`QS24AbX=i>)qA^_%r-ze
JbT{+h+@(uP{L-rCMMC*AF7-bQ#>_#K|Hw~t|eol%etR1?1L8>RiSJ>SErm^<Ez@s}mSQO$#h_+6LN;
2fo3*RhNgFs)VB%++Ao<zPKvXBdtLl&?pO%s3qKbwgbff4E(n%h`6@<U(Xtoxcf7ADvuWz4ZBIxW{F*
-}7HkO9KQH00008099TlP%PGxQ<x9{0FE~R03HAU0B~t=FJEbHbY*gGVQepBZ*FF3XLWL6bZKvHE^v9
xTYHb&HWL5epMs|#u#9SzrdJ%U27Gs$WRotk*(|bowD1|K)}n1TvLuModVN9ev){~+lqgDeHhlnR6j@
s$hr@aN=0Vo;yr+4#66?B*E0Jex8)xyFZ+TWR$*Z~;jjr=8XB98EBFoc!y`PRwSQc;jh_O@2cBQB)o-
vWJB@tpPk#ZTrpxZdDanyVK%VH_>rHCt@u$`zjELKEL*hjvHL6`6YC~R*;W=4o=EP;t7@#X6;A<mi*^
-{!Hg<LQxvUSSYE-w?7aJei6kXf_chL^zlhHKW$9%023VvZHDDA^L1UX}TF<ayp`^nksE8LK=^^BqzF
rj$4~d7UQghO?4y^IPCDhKDGeA{X!;B!Ek;>Z&ez2xPYVVn1cFD#fxo$qQUMPG`^KRPxbCY>T|CSeh^
6l()auYgp3!%%%Az_i{8s7Fi*RFuLVgl9!<rcOh~jnI5LLS;VE}r9B?l<0UK}^1CG`Mw%%;2#~Rk4V;
x_UIzW=&q1+IQ3jWJ^@LyKal(^eG#Of_u0+}_5f?=wN_lWx2of$pmU{Sy^UG(iKU@cl-xYC|)VP;}Q@
27c%|xC_kbDGd!Q8Cg9-dY03)HNh_v+`XpQEQgo;`gTy?J+ed4Bl<)Uz6RJSCYB)h-1kMEsm)`+z+Ig
$L{$mW*#w9<U1`;rAuqz1<h^^R+gGfW57Yl+)bFi2l5ZcS__}q(e6As5Eq6vj^;Y0}O0HPBj0e$P$>O
m-0RQ?FDFqumD;Y(bQ%Zu6cDq&-^Gtw~8Vd1%`Y1`t8}2y^8l>>mYtIYh}N8VDn(lH+2P1bC%`hHcrK
VIJy*40KZT8ibc%}qU)2-D(O8y(eWwxGw{St{(-#F3-G;H@kg$40rxFIZ0L9;U&mzvpdwkm0*|Z9C1*
a*Zbg}A<eGU&s53Ey=r56((Vq}p8Fo1dOJ1b$lKbOm9I)}pSj_-s(<oWRWhD`N{P79AoHlB;XwAQyE^
r%pmhM?m@)d|Q&A}ExLXswwfSYBe;BBPjkq8O+$G2b(5s2!jK+sy|@MB?k^Fj|KO#p-QTCO-cY6Mc30
NKD^Ylb9;mweBX9MAzLgFLGkC?q)oJJ=H;u|Zd`A5>w;ye^3=UT)$-vVC5&9iS~t0kxw|jMr&?0}l1+
^B5QdMa9WK+sTt~g%(h$jW&<VSisai*!Z2DOk633vPebcgB$|(SeYn7^hYpmGKmhlOEg!2{TM-54Ve)
fDCxYrK6^9s5LAGe{ybps(3`Fcz7#95q;W4UUOzd#n0acOYAkr$9(KBAA4H<u_WJzo+02uo;x@JUdr?
+(oG#dzWuzVQXP5719++@D4JQ(`T%BJ<PhVd?KYtNDKfgFL!=v}7Z)ggHF5+Dex0iU2F%fJ`j!;UP$d
l9Sv&++0XCQ_#f}zO77|lxKEaNGv6W^d5$J%588={U}BZ}+3Yqeyu2zYbEnxM5_Wxh&$nvx;`e9Rk*$
Ylu7zX^YZ5bEQ%fH`cp)&nNRa0ohrjwvCE-cZK}K5j(2^+I8)Jp>tm^*gIVYz@(m#od9mQ^23){uqhY
Bb$)rkN-QK1kDR#t1tBsAGf2N<pUiW2!Z(SUK|*~AP<&cd=FOgCcPb6D`<!N)Q}?Q36&#Ehcp>DL(v<
iZ0-tt;f_NegmHbj2JSZX)X!j)%M=i_iyeM`^D6+DHc7z!A3^wNVOA3B!b7Nx;;PJV!HFdxAEV@81z`
cPEnY4Gg)p`wCK4f)1lkFtPH~CS+l`P+F$aTgIYbZ$3oZ52t8+jkNN*~LZjyN>kHsVu!OepRxYt<#Jd
?Dptn!i*lBq1ZmpuzetAJQbq|Oq6FqoihUgNr1&9j+}F|(EAPBC!KJ0hT*S*Nl$Ijn?V>@Z=LFiRuQV
jKi}!<-m>Gh;lKdz7Y91TM8T`SE}xiJqp-lDLZ1{(%@WD<RJiO8|4NWVI6ttB}`;DvF>sNLK-j&Qp|7
0P#3ZA`H;8%RJ*&9B*LjCeI=NLdYTj!(q)JSr_2H9ZQ203YM6J&5Al-!%qYn5=qpoiTKvqdC+mA!19!
UR$Vl7032ExI^Mgq+ntcd9tx+OQ6#n(M31Oxi$e9c>z!ET4RD2S^Xao^qIi!U(F`CnA@JG8g%6n(q}?
vR^XbXs#bnZ(-+j{lLMewvk08kAYoj?-Tz9xF`1X4<!DQPMpB5v_6flQ?iV@s~5{87UB3Jtz)Kz5(PO
OH6-8CcgHc|xakcOWjo!i!+^sl}{Y`4B*m~Ti~?5btO8Zv7hK^8!XHN{d7Sdr-CppOkt3$L@uCwv)Wz
P7_0ofoVs<K;(GuPTn=@fu8{aXc!6yKAc21DE>L*`qGN0mv6*O!_yP?U0O`xu09zxOoHBLzq1TZY8u>
EF89Ux8WdHpFaNqT+vtJ2MW6$3)?(_gpMbch~|ry&KI}TA{p8(q1X^s^$`kC5X*1rf+^;M1NchVYSl|
N9cN4AKz5AxCpJK3R6STe+65$whP51kLMaVmn%okJM^zs21Ty=hJ8vAgsfje}Zzy3=-by(UMaGR-Z@8
==B#FEf)xPaaX_*Y}9;>smasfrC+6iSJuzz<;qf4%eAplINGJEU@DMr*|+#2K#Uh9rk=_0twxs=>cEX
tBlFl1bNe=`5J-Lz`ouycs@cZBqV)W}pCVM8*umB%G)Iu*9DcJ1AgcDH#ZSt_7tPry$?wbF!PD1dYz!
_AX&Qfd`7#J;SJj#!X38bG->D|9W1n9(T!FgLVIQ(D8O?Dbx7$f8U*q^^#epM-<#9am$^?;P0aDG#dh
A=MoU<=$lu3CVJUTZ1TV1!df;B?{RWMWFU}Kq92$L2P+Nrq_sOC~+GWj1qwE!)@YQ-ev-J#<arN6|ln
exQ?0s$c7(1!*WX(f0im+)BT!W-vwnh>P&gS^lovBn!ZUzhYeNpf*k0!+$NThUfQ&&Ctb$yqX)-H(i=
P)7zg_FJNq%(baMj5<-7}B3$i^Bfoa0qGq!R0F#?`V{PH^rv23c&2CV9sgSnRU4hj5uh6HLrx6sM*F>
(Bn-uC}z!f)t6f`p5VYdPz40DEYYvEaEywLyTMF?Awg4{P|mr)eVxDmp+`iS0M5Wz2R^sG1WKNXTH@z
4?P|X%5uXND=FLgd+#wx=(0`SrV;bNgWc<T0v9jZez5n9YyhNQSEy~^uP!r5~?5n_?lr8aFww7wNEd4
m=8D!_L%uy<M>3rPeDhL>nblObmP!tB-@0*5f{D&OYB>r`E+&AgRKFv+y`GedjZ?)uYLc@7C+u|C|y!
Wi_{^H>Wj0vNM?^0A-hU>EK%R;Fbc9^c2loIuSd$-Pr}nLqpKBr0inJweZP*izb@;t<W!%WY(dK9p2-
Rl>)#h&@jRphPz^e|B}-TI>Vzm1*(&$F52a8UT+SX!C@xn6F86?)5i^hgmS7afKEH#qM}}P`Hz#wx=~
}{fIvP?`9kP_j=LOG<<#;=9f~s2`46Aq!4b(KD2kKvTRf=1XCM)y0!pdI1Y&%H9vb?`4#cH5t==;-=f
CFU&6%M+HSlShYiXeDY=e1s=m6UL>V$hOEQyjX>%a3&CjiP%fo4OZy@&boREv0`IB?!6H@TL!{O!9hM
2;IWiHr7+t(l}HK+$RMv$B@qqHGzdJm>MNsc~Pszkj}&u-H=`90TRc`3u{Jcky9T-Ayab4CP=$J<nan
IKYi|c(-*o3y=veVkD7}FIP^O(qUkIwd)Kvtnq*mKzY_n``U8XVcaCgOsd_IMl$;(xr%7PHnm3KD#r)
gpW5`HnYz`QZ@Y}3T)5ReEDAVqFx_A9i6m;y4vN_O|XGu-o(}#D@YDtWxd&~wtgcMuWx&$V!hCye8CK
6~iny!PAgDG9R`)z<4hts&Bbme@djx_N$i~$K_keFV>++P~k{zY}a$?pef(Md$ZYNlI%InsA9TPyQ$M
}*2G!^dA{&dA|>;<$nvO*M)pEF3?SW9B!Fy@zsQqETSo0_uPIi4%VCAY5eiKtkjs^RyLYz;9JM5CWB4
Uvf?iH|^Cn0hf4Qp7iE)nyU>kgmD33FY%p}Y2pF{@uf;Khr0oQP`yl3qd9HJ199cKg?gxf03r)S8c1F
n@59GlZ~cazBTl@~QI+-5R7k!nOmqg5e}hRkWiUPIxeobLTP1Xp?t!MH1HfH$Zmz2&SYpYx${@0nK3b
bAR*h16yHmP3sFE)!qY>V*`#)B1wnYi$qN<8jXR1k_jVn6L1BxYA$`kOUuGkWOSG+mYQ>2<U$bJ{^14
PqJp0=lRp*8ebt|B`uD#*}Rb&5q`*5)qiKr_BI{w#y`?15Ob$Yr{z+K3YpBfWP!!k8pd<(j@LW&8|QS
xq?;C%$8?_|bLMyG$(egg@i>??A6kv3kup+f-E{r;i@3A?d1b@E+TvVqe6M3Q;@~Qr28P`u>N%{q;WO
&Cun#VT1(kWuDDEeWOP<=X#$$v*jiR0D|}|kDuM)M_oO{OJM32Qwa%C23rO_`P32^#!u@~gZ&|K&J=1
5R8|9G?pQX788dwTd*%K2AAY;MY4I8TJNcr^4<B><F-e+zx$U;O)ML#Y?g4gA5gUvfKtmVsyeX_WHFW
~@u`~<%@TL`q9g6z6iJ<48=b`TN!BdAX6d0FgQK^G~gBMo$LB&wZB;BtFTQH~F5V|x(_-gM9tHaeBK!
7c8Z)ITZumwX=cOujkXk#M-R}@bM^HVT$OS{9hkHs?8BIY@U$fgyHL6QW}^%iUZ&YD2_4c#96X81;CX
I{Ie)jD>apdDmcLC;#g`mm|JFQz47+KDk+^9(y&uyJ*39C8p#d>{o}QN2@_xG1r=g^5Blhao642p*ck
a8j-=LPR$_+6$g0q=P<+;%!OmzNkm5PMEof>kOTLKV6thsNHt8d!m1&>cDK=<*kpD^uk?}Hm_SF?5Cf
8nkw6e{~(SoH|pLFT6M*n<_+n#U+aC1a@{L|9UcFSjJAymbg;p*>)y>L*Mr-eD-~rki8_;1-~jGuL&B
k6!}Y7Pi;F3HW!mUX4*@9Dl}hMgsa2g3CHscOAXc-DY4D*2tmEjR`dVG)Ge!yS<d2=|bgV859V)XAA1
7#QXfK+~?b~(D(0&)TKhe5Y;`9a%-W9dQ6suD6CRUeGNIsBZ>U)I;&f07)%x#*1_JVrVx%X1=@&xZdI
yQyf^)_}YZ=yhM-Iv5BynD}q%oCq>k-*jgj&KrF>$M#~EhQdcp{omZRY_f!wEr&~RJ(3OLF&eC)FEcZ
clMxzT2=Rv2Be8EI<j1e3~+bPZq>DBFw~x>mSEx#fVWfxt9HVm64k}0fkpAf!U-z9qqL*gbL6ItU9gy
2UJ&gClt{YP!MlpIhEsvbrhYY*x^og>E3-WkmVE`bK!w9LROjO)4hr0>GcWAnVmer2FFoCN`!Qc}+3(
<S$anWW4(WLAJN>_a^lsL;m02fKmh+Rxi{BD*dZ$NLDcv+g4keY2=KEPU-8(Xdg%*R+{lNJYXs18C6T
OcgrworVEuJ3f$>@JjO9KQH0000804gAfPuA}kCS45x00$@l02=@R0B~t=FJEbHbY*gGVQepDcw=R7b
ZKvHb1ras)mm+D+c*;bo?k(@C~O0^_V)FI4>=&4CQY!Lw3nt`EVc_TEzveNvZxiMq`sp6{hk?85+&P7
7We54w6QI6I5V7i<{8q1!QkvutnyNu%!<mYM3n2oRI9bAN|DR>POj8oFgQATA#T@7EKQo42c4}%Y&IK
}mBM0VnuvuGh1!^V2$1;FY?R22#&exPA|_U4Rj3GJHrsqV6N$ExL`|!#+~z8oCTeMq&t+=W(b2Ln8!?
}|IrF*Do7@zokPB<ls#J6L*^kquDoSHgTMvuZQfCvff*JW@JAq!glJ)3Z=h6ILWr-;wt3TCqNC^IIY&
Z<+t0I$WRFyil5%eU({fw($-~Kv3y*NAlX@2wm`ug(v_0f@D?)iFlB=BOXT?ud4>oRShhsx!5t9hZUs
ft)NroGa(EcBwHiM?r!vW5DK{^1K-!o~H}OZV|c{Z(n~6t?c@=qOI5wc@SL&x*nnqb3x_PHAlXkJ2hy
K&bi|M}wbvYO<wXRfVJnPDU-P74ceSs*q_bfnp*KXNDrZo_|wfQWfmkU~(w*eWw2xu~l|R@U_X*l`3T
-OL<5v|Gkl#lIvluG9hDZsU^XKtFzmaS0}e817Qj=c>B}q>E-qLn}OJPnMk-oNS1IgIHE8rgjxKlV&q
De@T@<OXl1mPc3z7d4eLdR<3Erb$T6h;ZBZ!!5y7ODDxa7{){7CA5>{_?DvNYW3OmCaW5!YA34Vi2M{
?^-m-G3^s&qLaG$<#H(eq4hl=mOKUQptwnHYtJP6XbM#q?jSMKiYcH@#-LEaZlT&%}w?<EE%Twxhy~A
&=e(vt$%&wq>Dc``kvVq>)0eQ7kip!$W&Jj`k``j)+KAam*TbA9VD>h|cHGtuWDhb)N&-Ul<ZRd5`?&
{r;ndYDM9T6|4pJ!;)B{E&w4d&4k%{sbkq7kdvabIIR)@)y5PUn;{A|(rr_!?-a|uSA`|lQ@o_ciD-S
{VoHoUz8rFdef|>WLxt&-6-lt2GmIHVZqcrU{T`gO?w)jpkB{1Sb&iK|b8X6V(qOa$Q*FL?QoW<5Kxk
y9r08&Vltx&Hu*)q*7A-V~5ECG_J=dvvD+{X});wE@RgG-CwI+_M!lJqt3__iityp3WY+9zGP>UaxEk
C#oJV^^BldWG|C3_$*T%GgAAg-%?TAC^LpbZ72m8@BY&{jw%n#Jf^epe5foPv2EhMrjVUKeF0Q<dFQ`
bp+16nR*Mwt)TLEoJ=t5Qz6IDxA8R_b3-Mo<Ake30bTv_GY-k+d|!IQ`sLYohGkz@$99Bmb~O=bLC8R
T+-GpNEAY>0G63z+pVMbGS$g1Yo$^O8w&f!0>+Q0WmU>SKr^Cl6}44PWI{QykBJM$I*}bo7t*eIf_+T
JRh5=HM>ICWT~K7ihzdiofiI9l1QG-ZV0u^)jyYUw0#sxO;Qg~e)Zcz@XUIH9o%OXz1xod%MSh?g@+1
sXX!xb}3A50Bbf>n*soX3QDFE0iGDV__7L~}#IJI6YJ2%UDOw2c{>Fy|y2<#0c&FAd<`8?35(W<rt!l
E@&aJ*-T`c$&9(ZVEKloHZ~u)eEHI}>b}Cw7<fI6wTD4WmENA&huT$9b8_{-X-B>p(wu0k$97*_lia5
6<LC;R55`kbEp6`R|EXN}ZxJA@~N8X-4lF#pFs-kczv^JY>_AF^K^CS}W_6oW=JN2u!;QPC`_ex+M-;
9v6^L)(Zi%*doK1D7r|8Eg&;6Dn`RqY{dwTlqx(aSxXKXlsLoKi{g!9X_U=|s62)c1#N>WX~{;ETu{G
PW#~^bWR*9@IuL>os0RO{kwOYuTPf@7`iIkZjf_N52&pXA^ccQL6iUv6F4vJbNukXh1Xz!lE>$^lWgr
1P%m&$NOC38WMS<5SFp0=npdC4gK9j|s4dkiZk|FohdLmRyja}Rdpz^j^LAA{;Q#ye7o%U3DrfCt>Ld
W}d8zziLZ;NWaS^<?4H=WIiFaz(kZ5GO<CFmo%vxHHOShWq1^+*OCF>DgBtRdH@Mh>-%G20>U5p{9_I
8-3onq1QfODGO(VZzi9zPiQyZPyrwLF7Wr8V=hO;_U9F4^<_XK~mTXg|47L1S{+K9u?JF>UYL#NH6ve
#7hJ*wWKL4!8u0FLk<ITkjs)v9e8A1Xy++MyjyoT=hLnSq$OC#^Y|xsF)z%$x$A7=gk!Y>R=LS50D+n
Vr0xKDYkAL%$<Y+-nj%g|h3F{sRUdYS^!}wCikBXN0^OO9j-D<awWyc&W9CFT2qaf~I_q#b6t%O?Bm2
7R_0Yxr*atOu-saZ5Vrt;H{cH3b&kQQ7HVcr%N8JiPIUhjAn95E4L8uhDG^{cP;Tp|`4c32%Ex~=jQA
Q2?w_tzb0QmvXN714a<r)uJ)7L4eSP337wOb_nX1b8X+XAOenvVKG0fGsD5kaUC)X%Jq6Gw|sP~i*f`
4-J!^h0X?Bh1s$;8c<nUv*qzVJUE>Rb3)qV@k93pcC5zugU{57huh{*1X&s#wcwys3jnMHV9iH&p6)~
>Hm!<zy3R(BmzA9>Z|=8#gJ{^o9?ues-E{v&t>G6E6v9~Pq-*ks&!D9f^Y$M9ScjCw`1Qo9s7nC&Lmk
hVL@zJOsD?S)Z4r<iDLIUvuOOV+k|hN+U~HCk9I?^MB<`uhmg8pKAhOb?uhBQQZgP;-n)X~birFqWaS
}CjU*??B3|ozJn6}jF*SE7ZCnC&ktCj6*M|+3$=TLa#cp$J=}}J}bytjXa+7m;iNxq~NdmB+33rU>hp
71O_^<CQnXzUQnxq_TY6xZ!Bsx%)hK@#DQFr}$wr%KRPa5$q$=->^!|}oMvy~}9c;+;&i|+lp7z}jvk
)zH-@d(Lo^@2GQI!x*|$Mp^%?>d_OSz)K!jXHd!6|9J`3_d;1I9`ZXCV@X<U4Zw3m$_r?_PpreF}>dw
f9!pJ^5M<R<?Y%0;^f^$TTN<rA9qg=gBsH9T3&!iu#aLo4~M_r-~7CbQg+gCAsPz|SZOFmgL~2}F$aI
%wtM<gNM`AX9XF!ZmXEIbk{rtieb14?{_N3V5H>P4xvsn9y=z4sajjdL!Wz|9Fb4`f)P1sZ>K1yAy++
8vojUN%@~4vFnxY7j)@X#vD%Z(jNibrU&kgxV1YDpZ)Qt|!W=gP9U?l--m@q00CmaRiwsr0DHsm}7)$
vO^^USOE6CiqrWlRofu=DD~=JTiZ)2drz-uoVIe~}5x382$si?F$h^^zim>HrrZAf9gq;dNP$h*^}c+
Pfv_+inTEJXmh%VyY918^RMV>8=L!aL})4Yn`}o93NBPMOdF0Qg}ApDYrn{c)iaR{I_!>z?tV*kWA6x
dYZu!JlAy{qTlEPR|Iuv?DUFGcw^SaD;J4#K5#1(m#hc6h7_EwR8jZ$js=|%Vo-})8{$>&kiK(#-|G?
UefqAuPq!Cm@6N>AlhdD0UZ1@auil93H@D*I<o5JJ;F+NK