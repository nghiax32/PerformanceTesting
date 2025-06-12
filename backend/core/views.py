from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestRunSerializer
from .locust_utils import generate_locust_file, run_locust

class TestRunView(APIView):
    def post(self, request):
        serializer = TestRunSerializer(data=request.data)
        if serializer.is_valid():
            test_run = serializer.save()
            try:
                locust_file_path = generate_locust_file(test_run)
                log_path = run_locust(test_run, locust_file_path)
                test_run.status = "done"
                test_run.log_path = log_path
                test_run.save()
                return Response(TestRunSerializer(test_run).data)
            except Exception as e:
                test_run.status = "failed"
                test_run.save()
                return Response({"error": str(e)}, status=500)
        return Response(serializer.errors, status=400)