from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissions import IsModerator, IsOwner
from materials.serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import stripe
from django.conf import settings
from users.models import Payments
from .services import  create_session, create_price, create_product
from rest_framework import status


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с курсами (CRUD операции).
    """
    pagination_class = MaterialsPagination
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner | ~IsModerator]
        elif self.action == 'update':
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Представление для добавления урока
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    """
    Представление для просмотра уроков
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]
    pagination_class = MaterialsPagination



class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для просмотра конкретного урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для изменения урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления урока
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | ~IsModerator]


class SubscriptionAPIView(APIView):
    """
       Эндпоинт для управления подпиской пользователя на курс.
    """
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(owner=user, course=course_item)

            # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
            # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(owner=user, course=course_item)
            message = 'подписка добавлена'
            # Возвращаем ответ в API
        return Response({"message": message})


class PaymentCreateAPIView(APIView):
    """
    Создание платежа через Stripe.
    """
    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        try:
            product = create_product(course)
            price = create_price(product.id, course.price)
            session = create_session(price.id)
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payments.objects.create(
            user=request.user,
            paid_course=course,
            payment_amount=course.price,
            session_id=session.id,
            payment_url=session.url,
        )
        return Response({
            "payment_url": payment.payment_url,
            "session_id": payment.session_id
        })


class PaymentStatusAPIView(APIView):
    """
    Проверка статуса платежа в Stripe и синхронизация с локальной БД.
    """
    def get(self, request, session_id):
        session_id = session_id.strip()

        session = stripe.checkout.Session.retrieve(session_id)

        payment = get_object_or_404(Payments, session_id=session_id)

        if session.payment_status == "paid":
            payment.status = "paid"
            payment.save()

        return Response({
            "status": session.payment_status,
            "session_id": session.id
        })
