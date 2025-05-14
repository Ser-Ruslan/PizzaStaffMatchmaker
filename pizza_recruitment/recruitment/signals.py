from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Notification, Interview, UserRole, Restaurant

@receiver(post_save, sender=Application)
def application_notifications(sender, instance, created, **kwargs):
    # новая заявка
    if created:
        vacancy = instance.vacancy
        # уведомляем HR
        from django.contrib.auth import get_user_model
        User = get_user_model()
        hr_users = User.objects.filter(profile__role=UserRole.HR_MANAGER)
        for hr in hr_users:
            Notification.objects.create(
                user=hr,
                title=f"Новая заявка на «{vacancy.title}»",
                message=f"{instance.user.get_full_name()} подал(а) заявку на «{vacancy.title}»."
            )
        # уведомляем менеджеров нужных ресторанов
        for restaurant in vacancy.restaurants.all():
            if restaurant.manager:
                Notification.objects.create(
                    user=restaurant.manager,
                    title=f"Новая заявка на {vacancy.title}",
                    message=f"Поступила заявка от {instance.user.get_full_name()} на «{vacancy.title}».",
                )
    else:
        # изменение статуса
        old = Application.objects.get(pk=instance.pk)
        if old.status != instance.status:
            Notification.objects.create(
                user=instance.user,
                title="Обновлён статус заявки",
                message=f"Вашу заявку на «{instance.vacancy.title}» перевели в «{instance.get_status_display()}».",
            )

@receiver(post_save, sender=Interview)
def interview_notifications(sender, instance, created, **kwargs):
    if created:
        user = instance.application.user
        Notification.objects.create(
            user=user,
            title="Собеседование назначено",
            message=(
                f"Для вашей заявки «{instance.application.vacancy.title}» "
                f"назначено собеседование {instance.date_time.strftime('%d.%m.%Y %H:%M')}."
            )
        )
        if instance.interviewer:
            Notification.objects.create(
                user=instance.interviewer,
                title="Вас назначили интервьюером",
                message=(
                    f"Вас назначили интервьюером для {user.get_full_name()} "
                    f"по вакансии «{instance.application.vacancy.title}» "
                    f"{instance.date_time.strftime('%d.%m.%Y %H:%M')}."
                )
            )