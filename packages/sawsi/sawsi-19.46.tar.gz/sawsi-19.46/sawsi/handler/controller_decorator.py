"""
각 함수에 데코레이터를 적용하여 특정 경로로 라우팅되도록 만들기 위해 데코레이터를 정의합니다.
"""

controller_registry = {}

def controller(name=None):
    def decorator(func):
        # 모듈명과 함수명을 합쳐서 full_module_name 생성
        module_name = func.__module__
        func_name = func.__name__

        # name이 주어진 경우 해당 이름 사용, 아니면 기본 생성된 함수명 사용
        full_name = name or f"{module_name}.{func_name}"

        # controller_registry에 등록
        controller_registry[full_name] = func

        return func
    return decorator