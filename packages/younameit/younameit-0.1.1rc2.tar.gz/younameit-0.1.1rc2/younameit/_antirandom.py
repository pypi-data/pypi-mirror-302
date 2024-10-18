import contextlib
import random
import threading

thread_lock = threading.Lock()


@contextlib.contextmanager
def random_generator_poisoning(seed_value: bytes):
    """
    At the moment of this code scope execution - any function from the random
    package will return deterministic values.
    That's seriously dangerous. It can lead to security holes and data corruption.

    In multithreaded applications, there is a risk that this thread will be
    interrupted by any other thread while the pseudorandom generator is poisoned.
    Nothing can prevent it.
    However, this risk doesn't apply to single-threaded and async applications.

    If you are using a multithreaded design - do not run this function in
    the same Python process (same import scope) with any code that requires
    pseudorandom number generation.
    In such a case, start a sub-process for each `younameit` call.
    """

    assert isinstance(seed_value, bytes), f"Expecting the seed value to be bytes, not {type(seed_value)}"

    with thread_lock:
        old_seed = random.getstate()
        random.seed(seed_value, version=2)

        try:

            yield

            # If you're a brave developer and you know what you're doing,
            # do your best to at least open this context (`with` block),
            # just for one invocation of the poisoned random generator
            # and then close it immediately afterwards.

        finally:
            # Ensure that random-generators get back to normal.
            random.setstate(old_seed)
