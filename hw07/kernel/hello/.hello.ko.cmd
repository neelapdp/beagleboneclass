cmd_/home/debian/kernel/hello/hello.ko := ld -EL -r  -T ./scripts/module-common.lds --build-id  -T ./arch/arm/kernel/module.lds -o /home/debian/kernel/hello/hello.ko /home/debian/kernel/hello/hello.o /home/debian/kernel/hello/hello.mod.o