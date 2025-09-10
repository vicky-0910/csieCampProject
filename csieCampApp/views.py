from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from .models import TeamProfile, PointRecord, GameStatus, CommentBoard

CampUser = get_user_model()

def index(request):
    comments = CommentBoard.objects.order_by('-id')
    if request.method == "POST":
        comment = request.POST.get("comment")
        CommentBoard.objects.create(
            user = request.user,
            comment = comment
        )
    context = {
        "comments" : comments
    }
    return render(request, 'index.html',context)

def login_app(request):
    error = ""
    if request.user.is_authenticated:
	    return redirect("/")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            error = "帳號或密碼錯誤"
    return render(request, "login.html", {"error": error})

def logout_app(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("/")
    else:
        return redirect("/login/")

@login_required
def create_user(request):
    success_msg = ""
    error_msg = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if CampUser.objects.filter(username=username).exists():
            error_msg = "帳號名已存在，請換一個"
        else:
            user = CampUser.objects.create_user(
                username=username,
                password=password,
                role=role,
                is_active=True,
                is_staff=True if role == "admin" else False
            )
            success_msg = f"已創建帳號 {username}"
            if role == "team":
                TeamProfile.objects.create(user=user)
                success_msg += "，已建立該隊積分表"
    context = {
        "success_msg": success_msg,
        "error_msg": error_msg
    }

    return render(request, "create.html", context)

def password_change(request):
    success_msg = ""
    error_msg = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if CampUser.objects.filter(username=username).exists():
            user = CampUser.objects.get(username=username)
            user.set_password(password)
            user.save()
            success_msg = f"帳號 {username} 存在，密碼已更新"
        else:
            error_msg = f"帳號 {username} 不存在"
    context = {
        "success_msg": success_msg,
        "error_msg": error_msg
    }
    return render(request, "change.html", context)

#========= admin部分 =========
# control =========
@login_required
def control(request):
    if request.user.role != "admin":
        return redirect("/")

    num = ['一','二','三','四','五','六'] 
    debug_msg = ""
    team_list = [{"num": num[i-1],"team": TeamProfile.objects.get(user__username=f"team0{i}")} for i in range (1,7)]
    formid = "bingo" #預設顯示Bingo(for switch.js 提交後維持在提交處畫面)
    Bingotime = "尚未開始"
    Qnum_str = "1"
    if GameStatus.objects.filter(key="bingo_start").exists() :
        Bingotime = GameStatus.objects.get(key="bingo_start").value
    if GameStatus.objects.filter(key="question_num").exists() :
        Qnum_str = GameStatus.objects.get(key="question_num").value
        
    if request.method == "POST":
        formid = request.POST.get("formid")
        if formid == "bingo":
            first = 75000
            step = 5000
            teamscore = [{"id": i, "score": 0} for i in range(1,7)]
            if PointRecord.objects.filter(reason__startswith="Bingo").exists():
                debug_msg = "× Error: 勿重複提交Bingo成績"
            else :
                for i in range(1,7):
                    item = int(request.POST.get(f"item_{i}"))
                    line = int(request.POST.get(f"line_{i}"))
                    teamscore[i-1]['score'] = item *3 + line *10
                teamscore.sort(key=lambda x: x['score'], reverse=True)
                last_score = teamscore[0]['score']
                rank = 0
                for i in range(6):
                    if teamscore[i]['score'] < last_score:
                        rank += 1
                        last_score = teamscore[i]['score']
                    pt = first-step*rank
                    team = TeamProfile.objects.get(user__username=f"team0{teamscore[i]['id']}")
                    team.current_points += pt
                    team.save()
                    record = PointRecord.objects.create(
                        team=team,
                        change=pt,
                        reason=f"Bingo第{num[rank]}名",
                        balance=team.current_points,
                        modified_by=request.user
                    )
                debug_msg = "Accept: 完成提交Bingo成績"
        elif formid == "casinobank":
            i = request.POST.get("teamid")
            team = TeamProfile.objects.get(user__username=f"team0{i}")
            chip = int(request.POST.get("chip"))
            step = -500
            if team.fixed_savings == -1:
                debug_msg = f"× Error: 第{num[int(i)-1]}小隊尚未提交定存"
            elif team.current_points >= chip*step:
                pt = chip*step
                team.current_points += pt
                team.save()
                record = PointRecord.objects.create(
                    team=team,
                    change=pt,
                    reason=f"兌換{chip}個籌碼",
                    balance=team.current_points,
                    modified_by=request.user
                )
                debug_msg = f"第{num[int(i)-1]}小隊已兌換{chip}個籌碼"
            else :
                debug_msg = "× Error: 剩餘積分不足"
        elif formid == "casinoend":
            step = 500
            interest = 1.1
            if PointRecord.objects.filter(reason__startswith="積彈高").exists():
                debug_msg = "× Error: 勿重複提交提交賭場結算"
            else :
                for i in range(1,7):
                    team = team_list[i-1]['team']
                    chip = int(request.POST.get(f"chip_{i}"))
                    pt = chip*step + team.fixed_savings*interest
                    team.current_points += pt
                    team.fixed_savings = 0
                    team.save()
                    record = PointRecord.objects.create(
                        team=team,
                        change=pt,
                        reason=f"積彈高定存與籌碼",
                        balance=team.current_points,
                        modified_by=request.user
                    )
                    debug_msg = "Accept: 完成提交賭場結算"
        elif formid == "bonus":
            Qnum = int(Qnum_str)
            i = int(request.POST.get("teamid"))
            pt = int(request.POST.get("pt"))
            team = TeamProfile.objects.get(user__username=f"team0{i}")
            team.current_points += pt
            team.save()
            record = PointRecord.objects.create(
                team=team,
                change=pt,
                reason=f"答對Q.{Qnum}",
                balance=team.current_points,
                modified_by=request.user
            )
            debug_msg = f"第{num[i-1]}小隊答對Q.{Qnum}"
            Qnum += 1
            GameStatus.objects.update_or_create(
                key = "question_num",
                defaults={"value": Qnum}
            )
            
        elif formid == "other":
            debug_msg = "已修改："
            for i in range(1,7):
                if not request.POST.get(f"pt_{i}"):
                    continue
                elif not request.POST.get(f"reason_{i}"):
                    debug_msg = f"× Error: 第{num[i-1]}小隊原因為空"
                    break
                team = team_list[i-1]['team']
                pt = int(request.POST.get(f"pt_{i}"))
                team.current_points += pt
                team.save()
                record = PointRecord.objects.create(
                    team=team,
                    change=pt,
                    reason=request.POST.get(f"reason_{i}"),
                    balance=team.current_points,
                    modified_by=request.user
                )
                debug_msg += f"第{num[i-1]}小隊 "
            if len(debug_msg) < 5:
                debug_msg = "無修改"
        else :
            debug_msg = "未預期的錯誤"
        messages.info(request, debug_msg)
        #return redirect('control')
    messages.info(request, debug_msg)
    context = {
        "Bingotime" : Bingotime,
        "teams": team_list,
        "debug_msg" : debug_msg,
        "active_formid": formid,
        "Qnum": Qnum_str
    }
    return render(request, 'admin_control.html',context)

def bingostart(request):
    if request.user.role != "admin":
        return redirect("/")
    Bingotime = timezone.localtime(timezone.now()).strftime("%H:%M")
    GameStatus.objects.update_or_create(
        key="bingo_start",
        defaults={"value": Bingotime}
    )
    messages.success(request, f"遊戲開始時間：{Bingotime}")
    return redirect("/admin_control/")

# log&delete =========
from django.contrib import messages
from django.db import transaction

@login_required
def admin_log(request):
    if request.user.role != "admin":
        return redirect("/")
    record_list = PointRecord.objects.select_related("team__user", "modified_by").order_by('-id')
    team_list = [TeamProfile.objects.get(user__username=f"team0{i}") for i in range(1,7)]
    context = {
        "record_list": record_list,
        "teams": team_list,
    }
    return render(request, 'admin_log.html', context)

@login_required
def delete_record(request, record_id):
    if request.user.role != "admin":
        return redirect("/")
    if request.method != "POST":
        messages.error(request, "× Error")
        return redirect('admin_log')

    record = get_object_or_404(PointRecord, id=record_id)

    with transaction.atomic():
        team = record.team
        change_to_rollback = record.change
        record_pk = record.id
        if record.reason == "定存積分":
            team.fixed_savings = -1
        record.delete()

        later_records = PointRecord.objects.filter(team=team, id__gt=record_pk).order_by('id')

        for later in later_records:
            later.balance -= change_to_rollback
            later.save()

        latest = PointRecord.objects.filter(team=team).order_by('-id').first()
        team.current_points = latest.balance if latest else 0
        team.save()
    messages.success(request, f"已刪除紀錄（id={record_pk}），RollBack {change_to_rollback} 分。")

    return redirect('admin_log')

#========= team部分 =========
@login_required
def detail(request):
    if request.user.role != "team":
        return redirect("/")

    num = ['一','二','三','四','五','六']
    username = request.user.username
    teamid = int(username[-1:])
    current_pt = TeamProfile.objects.get(user__username=username).current_points
    num = ['一','二','三','四','五','六']
    team_name = f"第{num[teamid-1]}小隊"

    context = {
        "teamname": team_name,
        "username": username,
        "current_pt" : current_pt
    }
    return render(request, 'team_detail.html', context)

@login_required
def team_log(request):
    #return redirect("/")
    if request.user.role != "team":
        return redirect("/")
    num = ['一','二','三','四','五','六']
    username = request.user.username
    teamid = int(username[-1:])

    num = ['一','二','三','四','五','六']
    username = request.user.username
    teamid = int(username[-1:])
    current_pt = TeamProfile.objects.get(user__username=username).current_points
    num = ['一','二','三','四','五','六']
    team_name = f"第{num[teamid-1]}小隊"
    record_list = (
        PointRecord.objects
        .select_related("team__user", "modified_by")
        .filter(team__user__username=username)
        .order_by('-id')
    )
    context = {
        "teamname": team_name,
        "username": username,
        "current_pt" : current_pt,
        "record_list": record_list,
    }
    return render(request, 'team_log.html', context)

@login_required
def bingo(request):
    if request.user.role != "team":
        return redirect("/")
    Bingotime = "尚未開始"
    deltaminutes = 0
    if GameStatus.objects.filter(key="bingo_start").exists() :
        now = timezone.localtime(timezone.now())
        Bingotime = GameStatus.objects.get(key="bingo_start").value
        Bingotime_tocalc = datetime.datetime.strptime(Bingotime, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        Bingotime_tocalc = timezone.make_aware(Bingotime_tocalc, timezone.get_current_timezone())
        delta = now - Bingotime_tocalc
        deltaminutes = int(delta.total_seconds() // 60)
    context = {
        "Bingotime" : Bingotime,
        "deltaminutes" : deltaminutes
    }
    return render(request, 'bingorules.html',context)

@login_required
def casino(request):
    if request.user.role != "team":
        return redirect("/")
    username = request.user.username
    team = TeamProfile.objects.get(user__username=username)
    
    if request.method == "POST":
        fixed_value = int(request.POST.get("fixed"))
        if fixed_value > team.current_points:
            messages.error(request,  "× Error: 現有積分不足")
        elif team.fixed_savings != -1:
            messages.error(request,  "× Error: 已儲存定存")
        else :
            team.fixed_savings = fixed_value
            team.current_points -= team.fixed_savings
            team.save()
            record = PointRecord.objects.create(
                team=team,
                change=fixed_value*-1,
                reason=f"定存積分",
                balance=team.current_points,
                modified_by=request.user
            )
            messages.success(request,  "已完成定存")
        return redirect('casino')

    context = {
        "teamfixed" : team.fixed_savings
    }
    return render(request, 'casinorules.html',context)
    