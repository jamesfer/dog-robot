#include "listener.h"

template <class T, class P>
Listener<T, P>::Listener(
  T object,
  Listener<T, P>::ListenerFunction listenerFunction
): object(object), listenerFunction(listenerFunction) {}

template <class T, class P>
void Listener<T, P>::operator()(P payload) {
  (object).*(listenerFunction)(payload);
}
