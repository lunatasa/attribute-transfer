# -*- coding: utf-8 -*-
import maya.cmds as cmds

import maya.mel as mel

import math

import datetime

UVS_OpenFlag = [1]

UVS_matchingConditions = [1, 0, 0, 0]

UVS_transformOption = [0, 1, 0, 0, 0]

UVS_enableMatte = [1, 0]

orgOBJ = []

TargetOBJ = []


def UV_Shader_TransfWin():
    if cmds.window('UV_Shader_TransfWin', q=1, ex=1) == 1:
        cmds.showWindow('UV_Shader_TransfWin')
    cmds.window('UV_Shader_TransfWin', t='Batch Transform UV&Shader', s=0)

    cmds.columnLayout('UVS_MainCL', adj=1, p='UV_Shader_TransfWin')

    cmds.frameLayout('UVS_FirstFrame', p='UVS_MainCL', l='匹配条件', bs='etchedOut')

    cmds.rowLayout('First_row', nc=2, cw2=(120, 350), p='UVS_FirstFrame')

    cmds.checkBox('VEF_CB', l='Vertex  Edge  Face', v=UVS_matchingConditions[0], p='First_row', w=120,
                  cc='UVS_matchingConditions[0] = cmds.checkBox("VEF_CB",q = 1,v = 1)')

    cmds.rowLayout('Thr_row', nc=3, cw3=(100, 100, 150), p='First_row')

    cmds.checkBox('BB_CB', l='BoundingBox', p='Thr_row', w=100, v=UVS_matchingConditions[1],
                  cc='UVS_matchingConditions[1] = cmds.checkBox("BB_CB",q = 1,v = 1)')

    cmds.checkBox('Pos_CB', l='Position', p='Thr_row', w=100, v=UVS_matchingConditions[2],
                  cc='UVS_matchingConditions[2] = cmds.checkBox("Pos_CB",q = 1,v = 1)')

    cmds.checkBox('Name_CB', l='Name Without Prefix', p='Thr_row', w=150, v=UVS_matchingConditions[3],
                  cc='UVS_matchingConditions[3] = cmds.checkBox("Name_CB",q = 1,v = 1)')

    cmds.frameLayout('UVS_SecFrame', p='UVS_MainCL', l='传递选项', bs='etchedOut')

    cmds.rowLayout('Fourth_row', nc=5, cw5=(90, 90, 90, 90, 120), p='UVS_SecFrame')

    cmds.checkBox('UV_CB', l='UV', v=UVS_transformOption[0], p='Fourth_row', w=90,
                  cc='UVS_transformOption[0] = cmds.checkBox("UV_CB",q = 1,v = 1)')

    cmds.checkBox('Shader_CB', l='Shader', v=UVS_transformOption[1], p='Fourth_row', w=90,
                  cc='UVS_transformOption[1] = cmds.checkBox("Shader_CB",q = 1,v = 1)')

    cmds.checkBox('aiOpaque_CB', l='AiOpaque', v=UVS_transformOption[2], p='Fourth_row', w=90,
                  cc='UVS_transformOption[2] = cmds.checkBox("aiOpaque_CB",q = 1,v = 1)')

    cmds.checkBox('aiSubdivType_CB', l='AiSubdivsion', v=UVS_transformOption[3], p='Fourth_row', w=90,
                  cc='UVS_transformOption[3] = cmds.checkBox("aiSubdivType_CB",q = 1,v = 1)')

    cmds.checkBox('Displacement_CB', l='DisplacementShader', v=UVS_transformOption[4], p='Fourth_row', w=120,
                  cc='UVS_transformOption[4] = cmds.checkBox("Displacement_CB",q = 1,v = 1)')

    #cmds.checkBox('DisAttr_CB', l='Displacement Attributes', v=UVS_transformOption[5], p='Fourth_row', w=90,
                  #cc='UVS_transformOption[5] = cmds.checkBox("DisAttr_CB",q = 1,v = 1)')

    cmds.separator(p='UVS_MainCL')

    cmds.progressBar('UVS_prgBar', maxValue=100, h=10, p='UVS_MainCL')

    cmds.separator(p='UVS_MainCL')

    cmds.text('UVS_returnInfo', p='UVS_MainCL', l='')

    cmds.separator(p='UVS_MainCL')

    cmds.rowLayout('source_row', nc=5, cw5=(150, 30, 30, 30, 520), p='UVS_MainCL')

    cmds.button(l='导入原始物体>>', c='UVS_importObjects(0)', bgc=[0.2, 0.2, 0.2], w=150, p='source_row')

    cmds.button(l='+', c='UVS_addRemoveObjects(1,1)', bgc=[0.2, 0.2, 0.2], w=30, p='source_row')

    cmds.button(l='-', c='UVS_addRemoveObjects(0,1)', bgc=[0.2, 0.2, 0.2], w=30, p='source_row')

    cmds.text('UVS_sourNum', p='source_row', l=str(len(orgOBJ)), w=30, bgc=[0.2, 0.2, 0.2])

    cmds.textField('UVS_sourTF', ed=0, p='source_row', tx=str(orgOBJ), w=520)

    cmds.separator(p='UVS_MainCL')

    cmds.rowLayout('Target_row', nc=5, cw5=(150, 30, 30, 30, 520), p='UVS_MainCL')

    cmds.button(l='导入目标物体>>', c='UVS_importObjects(1)', bgc=[0.5, 0, 0], w=150, p='Target_row')

    cmds.button(l='+', c='UVS_addRemoveObjects(1,0)', bgc=[0.5, 0, 0], w=30, p='Target_row')

    cmds.button(l='-', c='UVS_addRemoveObjects(0,0)', bgc=[0.5, 0, 0], w=30, p='Target_row')

    cmds.text('UVS_TargetNum', l=str(len(TargetOBJ)), p='Target_row', w=30, bgc=[0.5, 0, 0])

    cmds.textField('UVS_TargetTF', ed=0, tx=str(TargetOBJ), p='Target_row', w=520)

    cmds.separator(p='UVS_MainCL')

    cmds.button(p='UVS_MainCL', l='开始传递', c='UVS_startTransfom()')

    cmds.frameLayout('UVS_otherFrame', p='UVS_MainCL', l='其他功能', collapsable=True, bs='etchedOut')

    cmds.rowLayout('other_row', nc=3, cw3=(100, 120, 90), p='UVS_otherFrame')

    cmds.checkBox('enableMatte', l='Enable Matte', v=UVS_enableMatte[0], p='other_row', w=100,
                  cc='UVS_enableMatte[0] = cmds.checkBox("enableMatte",q = 1,v = 1)')

    cmds.checkBox('disenableMatte', l='Disable Matte', v=UVS_enableMatte[1], p='other_row', w=120,
                  cc='UVS_enableMatte[1] = cmds.checkBox("disenableMatte",q = 1,v = 1)')

    cmds.button(p='other_row', l='执行', ann='框选物体后执行', c='UVS_switchEnableMatte()', w=50)

    cmds.showWindow('UV_Shader_TransfWin')


def UVS_addRemoveObjects(UVS_editMode, UVS_ObjectType_AR):
    getSelOBJ = cmds.ls(sl=1)

    screenObj = cmds.filterExpand(sm=12)

    if UVS_ObjectType_AR == 1:

        if UVS_editMode == 1:

            for i in screenObj:

                if i not in orgOBJ:
                    orgOBJ.append(i)

        elif UVS_editMode == 0:

            for i in screenObj:

                if i in orgOBJ:
                    orgOBJ.remove(i)

        cmds.textField('UVS_sourTF', e=1, tx=str(orgOBJ))

        cmds.text('UVS_sourNum', e=1, l=str(len(orgOBJ)))

    elif UVS_ObjectType_AR == 0:

        if UVS_editMode == 1:

            for i in screenObj:

                if i not in TargetOBJ:
                    TargetOBJ.append(i)

        elif UVS_editMode == 0:

            for i in screenObj:

                if i in TargetOBJ:
                    TargetOBJ.remove(i)

        cmds.textField('UVS_TargetTF', e=1, tx=str(TargetOBJ))

        cmds.text('UVS_TargetNum', e=1, l=str(len(TargetOBJ)))


def UVS_importObjects(UVS_objectType):
    getSelOBJ = cmds.ls(sl=1)

    screenObj = cmds.filterExpand(sm=12)

    if UVS_objectType == 1:

        cmds.textField('UVS_TargetTF', e=1, tx=str(screenObj))

        cmds.text('UVS_TargetNum', e=1, l=str(len(screenObj)))

        TargetOBJ[:] = []

        for i in screenObj:
            TargetOBJ.append(i)

    else:

        cmds.textField('UVS_sourTF', e=1, tx=str(screenObj))

        cmds.text('UVS_sourNum', e=1, l=str(len(screenObj)))

        orgOBJ[:] = []

        for i in screenObj:
            orgOBJ.append(i)


def UVS_startTransfom():
    cmds.progressBar('UVS_prgBar', e=1, pr=0)

    cmds.text('UVS_returnInfo', e=1, bgc=[0, 0, 0], l='正在传递..........稍候...')

    getTime = datetime.datetime(2011, 11, 0o1)

    startTime = getTime.today()

    p = 1.0

    for i in orgOBJ:

        prgValue = (p / len(orgOBJ)) * 100.0

        for k in TargetOBJ:

            checkValue = 0

            if UVS_matchingConditions[0] == 1:

                getOrgVerts = cmds.polyEvaluate(i, v=1)

                getOrgEdges = cmds.polyEvaluate(i, e=1)

                getOrgFaces = cmds.polyEvaluate(i, f=1)

                getTargetVerts = cmds.polyEvaluate(k, v=1)

                getTargetEdges = cmds.polyEvaluate(k, e=1)

                getTargetFaces = cmds.polyEvaluate(k, f=1)

                if getOrgVerts != getTargetVerts or getOrgEdges != getTargetEdges or getOrgFaces != getTargetFaces:

                    checkValue = 0
                else:

                    checkValue = 1

            if UVS_matchingConditions[1] == 1:

                getOrgBB = cmds.xform(i, q=1, bb=1)

                cacuOrgBBx = '%0.2f' % abs(getOrgBB[0] - getOrgBB[3])
                cacuOrgBBy = '%0.2f' % abs(getOrgBB[1] - getOrgBB[4])
                cacuOrgBBz = '%0.2f' % abs(getOrgBB[2] - getOrgBB[5])

                getTargetBB = cmds.xform(k, q=1, bb=1)

                cacuTargetBBx = '%0.2f' % abs(getTargetBB[0] - getTargetBB[3])
                cacuTargetBBy = '%0.2f' % abs(getTargetBB[1] - getTargetBB[4])
                cacuTargetBBz = '%0.2f' % abs(getTargetBB[2] - getTargetBB[5])

                if cacuOrgBBx != cacuTargetBBx or cacuOrgBBy != cacuTargetBBy or cacuOrgBBz != cacuTargetBBz:

                    checkValue = 0

                else:

                    checkValue = 1

            if UVS_matchingConditions[2] == 1:

                getOrgPos = cmds.xform(i, q=1, ws=1, piv=1)

                getTargetPos = cmds.xform(k, q=1, ws=1, piv=1)

                if math.floor(getOrgPos[0]) != math.floor(getTargetPos[0]) or math.floor(getOrgPos[1]) != math.floor(
                        getTargetPos[1]) or math.floor(getOrgPos[2]) != math.floor(getTargetPos[2]):

                    checkValue = 0

                else:

                    checkValue = 1

            if UVS_matchingConditions[3] == 1:

                splitTargetName = k.split(':')[-1]

                splitTargetNameAgain = splitTargetName.split('|')[-1]

                splitOrgName = i.split(':')[-1]

                splitOrgNameAgain = splitOrgName.split('|')[-1]

                if splitOrgNameAgain != splitTargetNameAgain:

                    checkValue = 0

                else:

                    checkValue = 1

            if checkValue == 1:

                if UVS_transformOption[2]:
                    getAiOp = cmds.getAttr(i + ".aiOpaque")
                    cmds.setAttr(k + ".aiOpaque", getAiOp)

                if 1 > 0:
                    height = cmds.getAttr(i + '.aiDispHeight')  # 获取置换高度
                    cmds.setAttr(k + '.aiDispHeight', height)  # 设置置换高度
                if 1 > 0:
                    padding = cmds.getAttr(i + '.aiDispAutobump')  # 获取置换自动凹凸
                    cmds.setAttr(k + '.aiDispAutobump', padding)  # 设置置换自动凹凸
                if 1 > 0:
                    scale = cmds.getAttr(i + '.aiDispPadding')  # 获取置换填充
                    cmds.setAttr(k + '.aiDispPadding', scale)  # 设置置换填充
                if 1 > 0:
                    scale = cmds.getAttr(i + '.aiDispZeroValue')  # 获取置换填充
                    cmds.setAttr(k + '.aiDispZeroValue', scale)  # 设置置换填充


                if UVS_transformOption[3]:
                    getAiSubType = cmds.getAttr(i + ".aiSubdivType")
                    getAiSubIter = cmds.getAttr(i + ".aiSubdivIterations")
                    cmds.setAttr(k + ".aiSubdivType", getAiSubType)
                    cmds.setAttr(k + ".aiSubdivIterations", getAiSubIter)

                if UVS_transformOption[4]:
                    getOriSGs = cmds.listConnections(cmds.listRelatives(i, shapes=1, f=1)[0], destination=1, source=0,
                                                     plugs=0, s=1, type="shadingEngine")
                    if len(getOriSGs) == 0:
                        print("%s not exist shader" % i)
                    getDis = cmds.listConnections("%s.displacementShader" % getOriSGs[0])
                    getTarSGs = cmds.listConnections(cmds.listRelatives(k, shapes=1, f=1)[0], destination=1, source=0,
                                                     plugs=0, s=1, type="shadingEngine")
                    getTarShader = cmds.listConnections("%s.surfaceShader" % getTarSGs[0])
                    dupShader = cmds.duplicate(getTarShader[0], ic=True)
                    cmds.select(k, r=True)
                    cmds.hyperShade(assign=dupShader[0])
                    newSG = cmds.listConnections("%s.outColor" % dupShader[0])
                    # cmds.connectAttr("%s.outColor"%dupShader[0],"%s.surfaceShader"%newSG, f=True)
                    cmds.connectAttr("%s.displacement" % getDis[0], "%s.displacementShader" % newSG[0], f=True)

                if UVS_transformOption[0] == 1:
                    cmds.polyTransfer(k, uv=1, ao=i)

                if UVS_transformOption[1] == 1:

                    getSGs = cmds.listConnections(cmds.listRelatives(i, shapes=1, f=1)[0], destination=1, source=0,
                                                  plugs=0, s=1, type="shadingEngine")

                    if len(getSGs) == 0:

                        print('error')

                    elif len(getSGs) == 1:

                        cmds.sets(cmds.listRelatives(k, shapes=1, f=1)[0], fe=getSGs[0])

                    else:

                        for m in getSGs[0:]:
                            UVS_assignShaderToObj(i, k, m)

        cmds.progressBar('UVS_prgBar', e=1, pr=prgValue)

        print(prgValue)

        ####break

        p = p + 1

    endTime = getTime.today()

    espTime = str(endTime - startTime)

    showInfo = '传递完成,用时【%s】' % espTime

    cmds.text('UVS_returnInfo', e=1, bgc=[0.5, 0.7, 1.0], l=showInfo)


def UVS_assignShaderToObj(sourceObject, TargetObject, sourceSG):
    getObjects = cmds.sets(sourceSG, q=1)

    facesForShadering = []

    try:

        for m in getObjects:

            if m.split('.')[0] == sourceObject:
                facesForShadering.append(TargetObject + '.' + m.split('.')[1])

            if len(facesForShadering) > 0:
                cmds.sets(facesForShadering, fe=sourceSG)

    except TypeError:

        pass


def UVS_switchEnableMatte():
    if UVS_enableMatte[0]:
        melCommand = '''
string $selObj[] = `ls -sl`;
string $renderLayer = `editRenderLayerGlobals -q -currentRenderLayer`;
for($i=0;$i<size($selObj);$i++)
{
    string $objshapes[] = `listRelatives -shapes -fullPath $selObj[$i]`;
    string $shaderGrp[] = `listConnections -type "shadingEngine" $objshapes[0]`;
    string $shader[] = `listConnections ($shaderGrp[0]+".surfaceShader")`;
    if(`attributeExists "aiEnableMatte" $shader[0]`)
    {
        if($renderLayer!="defaultRenderLayer")
        {editRenderLayerAdjustment ($shader[0]+".aiEnableMatte");}
        setAttr ($shader[0]+".aiEnableMatte") 1;
    }
    else
    {
        string $newAiShader = `createNode aiStandard`;
        setAttr ($newAiShader+".Kd") 0;
        setAttr ($newAiShader+".emission") 1;
        connectAttr ($shader[0]+".outColor") ($newAiShader+".emissionColor");
        connectAttr -force ($newAiShader+".outColor") ($shaderGrp[0]+".surfaceShader");

        if($renderLayer!="defaultRenderLayer")
        {editRenderLayerAdjustment ($shader[0]+".aiEnableMatte");}
        setAttr ($newAiShader+".aiEnableMatte") 1;
    }
}'''
        selObjList = cmds.ls(sl=True)
        for selobj in selObjList:
            objShape = cmds.listRelatives(selobj, shapes=True)[0]
            if cmds.nodeType(objShape) == "pfxHair":
                connectHair = cmds.listConnections(objShape, type="hairSystem")[0]
                hairShape = cmds.listRelatives(connectHair, shapes=True)[0]
                try:
                    aiHairShader = cmds.listConnections("%s.aiHairShader" % hairShape)[0]
                    cmds.setAttr("%s.aiEnableMatte" % aiHairShader, 1)
                    showInfo = '执行完成'
                    cmds.text('UVS_returnInfo', e=1, bgc=[0.5, 0.7, 1.0], l=showInfo)
                    cmds.warning('执行完成')
                except:
                    cmds.warning("%s 没有毛发材质" % hairShape)

            else:
                mel.eval(melCommand)
                showInfo = '执行完成'
                cmds.text('UVS_returnInfo', e=1, bgc=[0.5, 0.7, 1.0], l=showInfo)
                cmds.warning('执行完成')

    if UVS_enableMatte[1]:
        melCommand = '''
string $selObj[] = `ls -sl`;
string $renderLayer = `editRenderLayerGlobals -q -currentRenderLayer`;
for($i=0;$i<size($selObj);$i++)
{
    string $objshapes[] = `listRelatives -shapes -fullPath $selObj[$i]`;
    string $shaderGrp[] = `listConnections -type "shadingEngine" $objshapes[0]`;
    string $shader[] = `listConnections ($shaderGrp[0]+".surfaceShader")`;
    if(`attributeExists "aiEnableMatte" $shader[0]`)
    {
        if($renderLayer!="defaultRenderLayer")
        {editRenderLayerAdjustment ($shader[0]+".aiEnableMatte");}
        setAttr ($shader[0]+".aiEnableMatte") 0;
    }
}'''
        selObjList = cmds.ls(sl=True)
        for selobj in selObjList:
            objShape = cmds.listRelatives(selobj, shapes=True)[0]
            if cmds.nodeType(objShape) == "pfxHair":
                connectHair = cmds.listConnections(objShape, type="hairSystem")[0]
                hairShape = cmds.listRelatives(connectHair, shapes=True)[0]
                try:
                    aiHairShader = cmds.listConnections("%s.aiHairShader" % hairShape)[0]
                    cmds.setAttr("%s.aiEnableMatte" % aiHairShader, 0)
                    showInfo = '执行完成'
                    cmds.text('UVS_returnInfo', e=1, bgc=[0.5, 0.7, 1.0], l=showInfo)
                    cmds.warning('执行完成')
                except:
                    cmds.warning("%s 没有毛发材质" % hairShape)

            else:
                mel.eval(melCommand)
                showInfo = '执行完成'
                cmds.text('UVS_returnInfo', e=1, bgc=[0.5, 0.7, 1.0], l=showInfo)
                cmds.warning('执行完成')


UV_Shader_TransfWin()


