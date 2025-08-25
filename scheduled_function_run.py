import threading
import time
from datetime import datetime, timedelta

def printer(message):
    """
    Prints the provided message to the console.

    Args:
        message (str): The message to print.
    """
    print(message)


def run_in_thread(func, *args, **kwargs):
    """
    Runs the given function in a separate thread to prevent blocking the scheduler.

    Args:
        func (callable): The function to run.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Example:
        run_in_thread(printer, "Hello from the thread!")
    """
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()


def get_time_delta_seconds(hour, minute, second):
    """
    Calculates the number of seconds until the specified time (hour, minute, second) today.

    Args:
        hour (int): Target hour (0-23).
        minute (int): Target minute (0-59).
        second (int): Target second (0-59).

    Returns:
        float: Number of seconds until the specified time. Negative if the time has passed.
    """
    now = datetime.now()
    specified_time = datetime.combine(now.date(), datetime.time(hour, minute, second))
    return (specified_time - now).total_seconds()


def minute_interval_scheduled_function_run(minutes, seconds, func, *args, loop=True, **kwargs):
    """
    Runs the given function at specified intervals (every X minutes and Y seconds).
    The function is executed in a separate thread to avoid blocking.

    Args:
        minutes (int): Number of minutes in the interval.
        seconds (int): Number of seconds in the interval (will be added to minutes).
        func (callable): The function to run.
        *args: Positional arguments for the function.
        loop (bool): If True, runs in a loop at the specified interval. If False, executes only once after the interval.
        **kwargs: Keyword arguments for the function.

    Example:
        # Run every 5 minutes and 10 seconds
        interval_scheduled_function_run(5, 10, printer, "Scheduled function executed!", loop=True)
        
        # Run every 2 minutes and 30 seconds
        interval_scheduled_function_run(2, 30, printer, "Another scheduled function!", loop=True)
        
        # Run once after 1 minute and 15 seconds
        interval_scheduled_function_run(1, 15, printer, "One-time execution!", loop=False)
    """
    # Calculate total interval in seconds
    total_interval_seconds = (minutes * 60) + seconds
    
    print(f"Starting interval scheduler: every {minutes} minutes and {seconds} seconds")
    
    while True:
        print(f"Waiting for {minutes}m {seconds}s before next execution...")
        time.sleep(total_interval_seconds)
        
        print(f"Executing scheduled function...")
        run_in_thread(func, *args, **kwargs)
        
        if not loop:
            print("One-time execution completed.")
            break


def hourly_scheduled_function_run(hour, minute, second, func, *args, loop=True, **kwargs):
    """
    Runs the given function every hour at the specified time (minute, second), starting from the given hour.
    The function is executed in a separate thread to avoid blocking.

    Args:
        hour (int): Starting hour (0-23).
        minute (int): Minute to run the function (0-59).
        second (int): Second to run the function (0-59).
        func (callable): The function to run.
        *args: Positional arguments for the function.
        loop (bool): If True, runs in a loop every hour. If False, executes only once.
        **kwargs: Keyword arguments for the function.

    Example:
        hourly_scheduled_function_run(14, 30, 0, printer, "Scheduled function executed!", loop=True)
    """
    target = datetime.now().replace(hour=hour, minute=minute, second=second, microsecond=0)
    while True:
        now = datetime.now()
        if target <= now:
            target += timedelta(hours=1)
        delta_seconds = (target - now).total_seconds()
        print(f"Waiting for the next scheduled time: {target.strftime('%H:%M:%S')}")
        time.sleep(delta_seconds)
        run_in_thread(func, *args, **kwargs)
        if not loop:
            break
        target += timedelta(hours=1)


#temp
from datetime import datetime

if __name__ == "__main__":
    
    # Calculate time delta
    # seconds = get_time_delta_seconds(8, 50, 0)  
    # print(f"Time delta in seconds: {int(abs(seconds))}")

    current_hour = datetime.now().hour
    

    hourly_scheduled_function_run(current_hour, 52, 0, printer, "Scheduled function executed!", loop=True)