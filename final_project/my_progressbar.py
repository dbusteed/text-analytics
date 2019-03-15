import progressbar as pb

PBAR_DISPLAY = [pb.Percentage(), ' ', pb.Bar(marker='*', left='[', right=']'), ' ', pb.Timer()]

# used to handle / format multiple uses of progress bar
def start_pbar(max_val, msg='processing'):
    
    i = 0
    print(f'\n{msg}\n')

    # inti the pbar and start
    pbar = pb.ProgressBar(widgets=PBAR_DISPLAY, max_value=max_val, iterator=i)
    pbar.start()

    return pbar, i