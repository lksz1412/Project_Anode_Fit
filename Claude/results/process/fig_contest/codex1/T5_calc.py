for ratio, name in [(0.5,'A<0'), (1.0,'A=0'), (2.0,'A>0')]:
    xi = ratio/(ratio+1)
    flux = ratio*(1-xi)
    print(name, 'rplus/rminus=', ratio, 'xi_eq=', f'{xi:.4f}', 'flux=', f'{flux:.4f}',
          'forward=', f'(0,{ratio:.4f}) (1,0)', 'reverse=(0,0) (1,1)')
