def printer(message):
    """
    Prints the provided message to the console.

    Args:
        message (str): The message to print.
    """
    print(message)


def run_in_thread(func, *args, **kwargs):
    import threading
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
    from datetime import datetime, time
    """
    Calculates the number of seconds until the specified time (hour, minute, second) today.

    Args:
        hour (int): Target hour (0-23).
        minute (int): Target minute (0-59).
        second (int): Target second (0-59).

    Returns:
        float: Number of seconds until the specified time. Negative if the time has passed.
    """
    # Get current time
    now = datetime.now()
    # Create datetime object for specified time today
    specified_time = datetime.combine(now.date(), time(hour, minute, second))
    # Calculate delta
    delta = now - specified_time
    # Return total seconds (negative if specified time is in the past, positive if in the future)
    return delta.total_seconds()*-1


def hourly_scheduled_function_run(hour, minute, second, func, *args, **kwargs):
    import time
    """
    Runs the given function every hour at the specified time (hour, minute, second).
    The function is executed in a separate thread to avoid blocking.

    Args:
        hour (int): Hour to run the function (0-23).
        minute (int): Minute to run the function (0-59).
        second (int): Second to run the function (0-59).
        func (callable): The function to run.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Example:
        hourly_scheduled_function_run(14, 30, 0, printer, "Scheduled function executed!")
    """
    while True:

        delta_seconds = get_time_delta_seconds(hour, minute, second)

        if delta_seconds > 0:
            print(f"Waiting for the next scheduled time: {hour:02}:{minute:02}:{second:02}")
            time.sleep(int(abs(get_time_delta_seconds(hour, minute, second))))
            run_in_thread(func, *args, **kwargs)
            hour= (hour + 1)%24
        else:
            print("Waiting for the next day...")
            time.sleep(int(abs(get_time_delta_seconds(23, 59, 59)))+1)  # Adding 1 second to ensure it runs the next day
            pass



if __name__ == "__main__":
    
    # Calculate time delta
    # seconds = get_time_delta_seconds(8, 50, 0)  
    # print(f"Time delta in seconds: {int(abs(seconds))}")

    hourly_scheduled_function_run(9, 15, 0, printer, "Scheduled function executed!")