# Disassembly Report

**Binary:** `/opt/benchmark/hello-world/b-gr740/app.exe`

**Functions Extracted:** foo, Init


## foo
```
00001258 <foo>:
    1258:	83 3a 20 1f 	sra  %o0, 0x1f, %g1
    125c:	90 18 40 08 	xor  %g1, %o0, %o0
    1260:	81 c3 e0 08 	retl 
    1264:	90 20 40 08 	sub  %g1, %o0, %o0

```

## Init
```
00001268 <Init>:
    1268:	9d e3 bf a0 	save  %sp, -96, %sp
    126c:	92 10 20 00 	clr  %o1
    1270:	3b 00 00 7c 	sethi  %hi(0x1f000), %i5
    1274:	40 00 02 fd 	call  1e68 <rtems_test_begin>
    1278:	90 17 60 60 	or  %i5, 0x60, %o0	! 1f060 <rtems_test_name>
    127c:	7f ff ff f7 	call  1258 <foo>
    1280:	90 10 20 03 	mov  3, %o0
    1284:	80 a2 20 03 	cmp  %o0, 3
    1288:	24 80 00 09 	ble,a   12ac <Init+0x44>
    128c:	11 00 00 6e 	sethi  %hi(0x1b800), %o0
    1290:	11 00 00 6e 	sethi  %hi(0x1b800), %o0
    1294:	40 00 60 09 	call  192b8 <puts>
    1298:	90 12 20 30 	or  %o0, 0x30, %o0	! 1b830 <rtems_libio_number_iops+0xc>
    129c:	40 00 03 00 	call  1e9c <rtems_test_end>
    12a0:	90 17 60 60 	or  %i5, 0x60, %o0
    12a4:	40 00 62 1d 	call  19b18 <exit>
    12a8:	90 10 20 00 	clr  %o0
    12ac:	40 00 60 03 	call  192b8 <puts>
    12b0:	90 12 20 38 	or  %o0, 0x38, %o0
    12b4:	30 bf ff fa 	b,a   129c <Init+0x34>

```
