from functools import wraps,partial
from settings import logging
import time

logger = logging.getLogger(__name__)



def Counter(func):
    """Decorator for counting timer."""
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            ans = func(*args, **kwargs)
            logger.debug(f'Running func:{func.__name__} for {wrapper.calls} times.')
            wrapper.calls += 1
            return ans
        except Exception as e:
            logger.critical(e)
            logger.critical(f'{func.__name__} cannot work.')
    wrapper.calls=1
    return wrapper


def Timer(func):
    """Decorator for timming timer."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        ans = func(*args, **kwargs)
        end_time = time.perf_counter()
        running_time = end_time-start_time
        logger.debug(f'func:{func.__name__} running in {running_time:.4f} sec.')
        return ans
    return wrapper
    

def Retry_timer(func,interval=3,retry_times=3):
    """Decorator for retry func."""
    # TODO:: add func for user to input interval and retry_times
    @wraps(func)
    def wrapper(count=1, interval=interval, retry_times=retry_times, *args, **kwargs):
        try:
            logger.debug(f'Try func:{func.__name__} {count} times.')
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f'There have some error: {e}')
            count += 1
            if count <= retry_times:
                logger.debug(f'Will retry in {interval} sec.')
                time.sleep(interval)
                return wrapper(count=count,interval=interval, retry_times=retry_times,*args,**kwargs)
            else:
                logger.critical(f'Failed to execute func:{func.__name__}')
    return wrapper


