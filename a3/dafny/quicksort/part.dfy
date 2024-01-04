include "preds.dfy"

method choose(l:nat, u:nat) returns (rv: nat)
  requires l <= u;
  ensures l <= rv <= u;
{
  rv := l;
  assume(l <= rv <= u);
}

method partition(a:array<int>, l:nat, u:nat) returns (pivot:int)
  modifies a;
  requires a != null;
  requires l <= u < a.Length;
  requires l>0 ==> partitioned(a, 0, l-1, l, u);
  requires u+1 <= a.Length -1 ==> partitioned(a, l, u, u+1, a.Length-1);

  ensures l <= pivot <= u;

  ensures l > 0 ==> beq(old(a[..]), a[..], 0, l-1);
  ensures l > 0 ==> partitioned(a, 0, l-1, l, u);

  ensures u < a.Length-1 ==> beq(old(a[..]), a[..], u+1, a.Length - 1);
  ensures u < a.Length - 1 ==> partitioned(a, l, u, u+1, a.Length-1);

  ensures pivot > l ==> partitioned(a, l, pivot-1, pivot, pivot);
  ensures pivot < u ==> partitioned(a, pivot, pivot, pivot+1, u);
{
  var pi := choose(l, u);
  var pv := a[pi];

  a[pi] := a[u];
  a[u] := pv;

  var i:int := l - 1;
  var j := l;
  while (j < u)
  invariant l - 1 <= i < j <= u;
  invariant a[u] == pv;
  invariant forall k :: l <= k <= i ==> a[k] <= a[u];
  invariant forall k :: i < k < j ==> a[k] > a[u];
  // invariant forall k :: j < k < u ==> a[k] == old(a[k])
  invariant forall k :: u < k < a.Length ==> a[k] == old(a[k])
  invariant forall k :: 0 <= k < l ==> a[k] == old(a[k])
  invariant forall i,j :: 0 <= i < l && u < j < a.Length ==> a[i] <= a[j]
  invariant forall i,j :: l <= i <= u && u + 1 <= j <= a.Length - 1 ==> a[i] <= a[j]
  invariant forall i,j :: 0 <= i <= l - 1 && l <= j <= u ==> a[i] <= a[j]
  {
    if (a[j] <= pv)
    {
      i := i + 1;
      var t := a[i];
      a[i] := a[j];
      a[j] := t;
    }
    j := j + 1;
  }

  pivot := i + 1;
  var t := a[pivot];
  a[pivot] := a[u];
  a[u] := t;
}
