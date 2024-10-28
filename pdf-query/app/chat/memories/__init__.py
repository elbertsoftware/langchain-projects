from .full_memory import build_full_memory
from .window_memory import build_window_memory


memory_map = {
  'sql_full_memory': build_full_memory,
  'sql_window_memory': build_window_memory
}