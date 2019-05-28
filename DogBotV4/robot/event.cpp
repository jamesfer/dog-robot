#include "event.h"

template<class P, int L>
void Event<P, L>::fire(P payload) {
  for (int i = 0; i < listenerCount; i++) {
    listeners[i](payload);
  }
}

template<class P, int L>
void Event<P, L>::listen(Event<P, L>::ListenerFunction listener) {
  if (listenerCount < L) {
    listeners[listenerCount] = listener;
    listenerCount += 1;
  }
}
