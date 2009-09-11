// counter.c
// second eg from 'how to write Pure Data externals'
// nks 6 sep 2009

#include "m_pd.h"

static t_class *counter_class;

typedef struct _counter {
  t_object x_obj;
  t_int i_count;
} t_counter;

void counter_bang(t_counter *x) {
  // want to output the value before incrementing, hence tmp var
  t_float f = x->i_count;

  x->i_count++;

  outlet_float(x->x_obj.ob_outlet, f);
}

void *counter_new(t_floatarg f) {
  t_counter *x = (t_counter *)pd_new(counter_class);

  x->i_count = f;
  outlet_new(&x->x_obj, &s_float); // what is s_float?

  return (void *)x;
}

void counter_setup(void) {
  counter_class = class_new(gensym("counter"),
  (t_newmethod)counter_new,
  0, sizeof(t_counter),
  CLASS_DEFAULT,
  A_DEFFLOAT, 0); // that first arg defaults to 0

  class_addbang(counter_class, counter_bang);
}


