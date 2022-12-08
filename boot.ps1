Set PYTHONIOENCODING="UTF-8"

for ($num = 1 ; $num -le 200 ; $num++)
{
    echo "******************* Loop = $num *******************"
    pyluos-bootloader flash -t 2 3 4 5 6 7 8 -b salem.bin
    pyluos-bootloader detect
    sleep 5
    pyluos-bootloader reset
}
