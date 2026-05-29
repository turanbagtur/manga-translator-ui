#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Manga Ceviri Baslatic Betigi
Manga Translator UI Launcher
"""

import os
import sys
import argparse
import subprocess
import importlib.util
from pathlib import Path

# 项目配置
BRANCH = 'main'
VERSION = '1.7.6'
PYTHON_VERSION_MIN = (3, 12)
PYTHON_VERSION_MAX = (3, 12)  # 仅支持Python 3.12,不支持3.13+

# 路径配置
PATH_ROOT = Path(__file__).parent.parent
stored_commit_hash = None

# 获取环境变量
python = sys.executable

# Git路径配置 (优先使用便携版)
portable_git = PATH_ROOT / "PortableGit" / "cmd" / "git.exe"
if portable_git.exists():
    git = str(portable_git)
else:
    git = os.environ.get('GIT', "git")

skip_install = False
index_url = os.environ.get('INDEX_URL', "")

# 备用镜像源列表（按优先级排序）
MIRROR_URLS = [
    "https://pypi.tuna.tsinghua.edu.cn/simple/",  # 清华源
    "https://mirrors.aliyun.com/pypi/simple/",     # 阿里云
    "https://pypi.douban.com/simple/",             # 豆瓣
    "https://pypi.org/simple/",                    # 官方源（作为最后备选）
]


def is_python_version_valid():
    """检查Python版本是否符合要求"""
    if sys.version_info < PYTHON_VERSION_MIN:
        print(f'Hata: Python gerekli {PYTHON_VERSION_MIN[0]}.{PYTHON_VERSION_MIN[1]}+ ')
        print(f'当前Surum: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
        return False
    if sys.version_info[:2] > PYTHON_VERSION_MAX:
        print(f'Hata: Sadece Python {PYTHON_VERSION_MAX[0]}.{PYTHON_VERSION_MAX[1]}, daha yuksek surum desteklenmez')
        print(f'当前Surum: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
        print(f'Lutfen Python kullanin {PYTHON_VERSION_MAX[0]}.{PYTHON_VERSION_MAX[1]} surumu')
        return False
    return True


def is_installed(package):
    """检查Python包是否已安装"""
    try:
        spec = importlib.util.find_spec(package)
    except ModuleNotFoundError:
        return False
    return spec is not None


def run(command, desc=None, errdesc=None, custom_env=None, live=False, timeout=None, capture_output=True):
    """执行系统命令
    
    Args:
        command: 要执行的命令
        desc: 描述信息
        errdesc: 错误描述
        custom_env: 自定义环境变量
        live: 是否实时显示输出（不捕获）
        timeout: 超时时间（秒），None 表示无超时
        capture_output: 是否捕获输出，False 时丢弃输出避免死锁
    """
    if desc is not None:
        print(desc)

    env = os.environ if custom_env is None else custom_env

    if live:
        # 实时模式：直接显示输出
        result = subprocess.run(command, shell=True, env=env)
        if result.returncode != 0:
            raise RuntimeError(f"""{errdesc or '命令执行错误'}.
命令: {command}
错误代码: {result.returncode}""")
        return ""

    if not capture_output:
        # 不捕获输出模式：丢弃输出避免死锁
        result = subprocess.run(
            command, 
            shell=True, 
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout
        )
        if result.returncode != 0:
            raise RuntimeError(f"""{errdesc or '命令执行错误'}.
命令: {command}
错误代码: {result.returncode}""")
        return ""

    # 捕获输出模式：使用 Popen + communicate 避免死锁
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # communicate() 会同时读取 stdout 和 stderr，避免死锁
        stdout_bytes, stderr_bytes = process.communicate(timeout=timeout)
        
        # 解码输出
        try:
            stdout = stdout_bytes.decode('utf-8', errors='ignore')
        except:
            try:
                stdout = stdout_bytes.decode('gbk', errors='ignore')
            except:
                stdout = str(stdout_bytes)
        
        try:
            stderr = stderr_bytes.decode('utf-8', errors='ignore')
        except:
            try:
                stderr = stderr_bytes.decode('gbk', errors='ignore')
            except:
                stderr = str(stderr_bytes)
        
        if process.returncode != 0:
            message = f"""{errdesc or '命令执行错误'}.
命令: {command}
错误代码: {process.returncode}
stdout: {stdout if stdout else '<empty>'}
stderr: {stderr if stderr else '<empty>'}
"""
            raise RuntimeError(message)
        
        return stdout
        
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()  # 清理剩余输出
        raise RuntimeError(f"""{errdesc or '命令超时'}.
命令: {command}
超时: {timeout}秒""")


def run_pip(args, desc=None):
    """使用pip安装包，支持多镜像源自动回退"""
    if skip_install:
        return
    
    import urllib.parse
    
    def build_pip_command(pip_args, mirror_url=None):
        """构建pip命令"""
        index_url_line = f' --index-url {mirror_url}' if mirror_url else ''
        trusted_host_line = ''
        
        if mirror_url:
            parsed = urllib.parse.urlparse(mirror_url)
            if parsed.hostname:
                trusted_host_line += f' --trusted-host {parsed.hostname}'
            trusted_host_line += ' --trusted-host download.pytorch.org'
        
        return f'"{python}" -m pip {pip_args} --prefer-binary{index_url_line}{trusted_host_line} --disable-pip-version-check --no-warn-script-location'
    
    # 如果用户指定了 INDEX_URL，优先使用
    if index_url:
        mirrors_to_try = [index_url] + [m for m in MIRROR_URLS if m != index_url]
    else:
        mirrors_to_try = MIRROR_URLS.copy()
    
    last_error = None
    for i, mirror in enumerate(mirrors_to_try):
        try:
            mirror_name = urllib.parse.urlparse(mirror).hostname or mirror
            if i == 0:
                print(f"Kuruluyor: {desc}...")
            else:
                print(f"Yedek kaynak deneniyor: {mirror_name}")
            
            cmd = build_pip_command(args, mirror)
            result = subprocess.run(cmd, shell=True, env=os.environ)
            
            if result.returncode == 0:
                return ""
            else:
                last_error = f"返回码: {result.returncode}"
                print(f"Kaynak {mirror_name} kurulum basarisiz, {last_error}")
                
        except Exception as e:
            last_error = str(e)
            print(f"Kaynak {mirror_name} hatasi: {last_error}")
    
    # 所有镜像源都失败
    raise RuntimeError(f"Kurulamadi: {desc}, tum kaynaklar basarisiz。最后错误: {last_error}")


def run_pip_requirements(requirements_file, desc=None):
    """逐个安装requirements文件中的包，失败时从失败的包开始切换镜像重试"""
    if skip_install:
        return
    
    import urllib.parse
    from pathlib import Path
    
    # 读取 requirements 文件
    req_path = Path(requirements_file)
    if not req_path.exists():
        raise RuntimeError(f"找不到依赖文件: {requirements_file}")
    
    # 解析 requirements 文件，提取有效的包和索引源
    packages = []
    primary_index_url = None  # 存储 --index-url 参数（主源）
    extra_index_urls = []  # 存储 --extra-index-url 参数（launch.py 中忽略，仅供 pip 直接安装时使用）
    
    with open(req_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行、注释
            if not line or line.startswith('#'):
                continue
            # 解析 --extra-index-url 选项（忽略，不添加到 extra_index_urls）
            if line.startswith('--extra-index-url'):
                # 完全忽略 --extra-index-url，让 torch 相关包只能从主源下载
                continue
            # 解析 --index-url 选项（主源）
            if line.startswith('--index-url'):
                parts = line.split(None, 1)
                if len(parts) == 2:
                    primary_index_url = parts[1].strip()
                continue
            # 跳过其他 pip 选项
            if line.startswith('-'):
                continue
            # 去除行内注释
            line = line.split('#')[0].strip()
            if line:
                packages.append(line)
    
    # 需要从 PyTorch 源下载的包列表（包括 PyTorch 及其依赖）
    pytorch_packages = [
        'torch', 'torchvision', 'torchaudio', 'xformers',
        # PyTorch 核心依赖
        'pytorch-triton', 'pytorch-triton-rocm', 'pytorch-triton-xpu',
        'torch-cuda80', 'torch-model-archiver', 'torch-tb-profiler',
        'torch-tensorrt', 'torchao', 'torchaudio', 'torchcodec',
        'torchcsprng', 'torchdata', 'torchmetrics', 'torchrec',
        'torchrec-cpu', 'torchserve', 'torchtext', 'torchvision',
        # NVIDIA CUDA 相关
        'nvidia-cublas-cu12', 'nvidia-cuda-cupti-cu12', 'nvidia-cuda-nvrtc-cu12',
        'nvidia-cuda-runtime-cu12', 'nvidia-cudnn-cu11', 'nvidia-cudnn-cu12',
        'nvidia-cudnn-cu13', 'nvidia-cufft-cu12', 'nvidia-cufile-cu12',
        'nvidia-curand-cu12', 'nvidia-cusolver-cu12', 'nvidia-cusparse-cu12',
        'nvidia-cusparselt-cu12', 'nvidia-nccl-cu12', 'nvidia-nvjitlink-cu12',
        'nvidia-nvshmem-cu12', 'nvidia-nvtx-cu12',
        # Intel oneAPI 相关
        'intel-cmplr-lib-rt', 'intel-cmplr-lib-ur', 'intel-cmplr-lic-rt',
        'intel-opencl-rt', 'intel-openmp', 'intel-pti', 'intel-sycl-rt',
        'oneccl', 'oneccl-devel', 'onemkl-sycl-blas', 'onemkl-sycl-dft',
        'onemkl-sycl-lapack', 'onemkl-sycl-rng', 'onemkl-sycl-sparse',
        # 其他 PyTorch 生态依赖
        'triton', 'fbgemm-gpu', 'fbgemm-gpu-genai', 'flashinfer',
        'flashinfer-python', 'vllm', 'cuda-bindings', 'dpcpp-cpp-rt',
        'mpi-rt', 'tcmlib'
    ]
    
    # 需要忽略版本限制的包（安装时去掉版本号，安装最新兼容版本）
    # 注意：功能已在下方逻辑中禁用
    ignore_version_packages = [
        'xformers',        # PyTorch 扩展，必须与 torch surumu匹配
        'transformers',    # 与 PyTorch surumu强相关，避免 torch._C 模块错误
        'accelerate',      # transformers 的加速库
        'timm',            # 图像模型库，依赖 PyTorch
        'kornia',          # 计算机视觉库，依赖 PyTorch
        'spandrel',        # 神经网络架构库，依赖 PyTorch
        'open_clip_torch'  # CLIP 模型，依赖 PyTorch
    ]
    
    # PyTorch 核心包版本锁定（暂时禁用）
    # locked_versions = {
    #     'torch': '2.9.1',
    #     'torchvision': '0.22.1',
    #     'torchaudio': '2.6.1',
    # }
    locked_versions = {}
    
    def is_pytorch_package(pkg_name):
        """检查是否是需要从 PyTorch 源下载的包"""
        pkg_lower = pkg_name.lower()
        
        # 排除不应该从 PyTorch 源下载的包（即使名字以 torch 开头）
        excluded_packages = ['torchsummary', 'torchmetrics']
        if pkg_lower in excluded_packages:
            return False
        
        for prefix in pytorch_packages:
            if pkg_lower.startswith(prefix):
                return True
        return False
    
    def build_pip_command(pip_args, mirror_url=None, use_primary_index=False):
        """构建pip命令
        
        Args:
            pip_args: pip 命令参数
            mirror_url: Kaynak URL（用于非 PyTorch 包）
            use_primary_index: 是否使用 requirements 文件中指定的主源（用于 PyTorch 包）
        """
        index_url_line = ''
        extra_index_line = ''
        trusted_host_line = ''
        
        # PyTorch 包：使用 requirements 文件中的 --index-url 作为主源
        if use_primary_index and primary_index_url:
            index_url_line = f' --index-url {primary_index_url}'
            parsed_primary = urllib.parse.urlparse(primary_index_url)
            if parsed_primary.hostname:
                trusted_host_line += f' --trusted-host {parsed_primary.hostname}'
            # 添加 extra-index-url 作为备用源（用于其他依赖）
            for extra_url in extra_index_urls:
                extra_index_line += f' --extra-index-url {extra_url}'
                parsed_extra = urllib.parse.urlparse(extra_url)
                if parsed_extra.hostname:
                    trusted_host_line += f' --trusted-host {parsed_extra.hostname}'
        else:
            # 非 PyTorch 包：使用镜像源
            if mirror_url:
                index_url_line = f' --index-url {mirror_url}'
                parsed = urllib.parse.urlparse(mirror_url)
                if parsed.hostname:
                    trusted_host_line += f' --trusted-host {parsed.hostname}'
        
        trusted_host_line += ' --trusted-host download.pytorch.org'
        
        return f'"{python}" -m pip {pip_args} --prefer-binary{index_url_line}{extra_index_line}{trusted_host_line} --disable-pip-version-check --no-warn-script-location'
    
    if not packages:
        print(f"[警告] {requirements_file} 中没有找到有效的依赖包")
        return
    
    # 如果用户指定了 INDEX_URL，优先使用
    if index_url:
        mirrors_to_try = [index_url] + [m for m in MIRROR_URLS if m != index_url]
    else:
        mirrors_to_try = MIRROR_URLS.copy()
    
    total = len(packages)
    print(f"Kuruluyor: {desc or requirements_file}... (共 {total} paket daha)")
    
    # 当前镜像索引
    current_mirror_idx = 0
    # 当前包索引
    pkg_idx = 0
    
    while pkg_idx < total:
        pkg = packages[pkg_idx]
        mirror = mirrors_to_try[current_mirror_idx]
        mirror_name = urllib.parse.urlparse(mirror).hostname or mirror
        
        # 获取包名用于显示（去除版本约束）
        pkg_display = pkg.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].split('@')[0].strip()
        print(f"[{pkg_idx + 1}/{total}] Kuruluyor: {pkg_display}...")
        
        # 检查是否是 PyTorch 相关包，需要使用主源
        use_primary = is_pytorch_package(pkg_display) and primary_index_url
        
        # 检查是否需要忽略版本限制
        pkg_to_install = pkg
        pkg_lower = pkg_display.lower()
        
        # surumu锁定和忽略版本限制功能已禁用，按 requirements 文件版本安装
        # if pkg_lower in locked_versions:
        #     pkg_to_install = f"{pkg_display}=={locked_versions[pkg_lower]}"
        #     print(f"    (版本锁定: {locked_versions[pkg_lower]})")
        # elif pkg_lower in ignore_version_packages or use_primary:
        #     pkg_to_install = pkg_display
        #     print(f"    (忽略版本限制，安装最新版)")
        
        if use_primary:
            print(f"    (使用 PyTorch 源: {primary_index_url})")
        
        cmd = build_pip_command(f'install "{pkg_to_install}"', mirror, use_primary_index=use_primary)
        
        try:
            result = subprocess.run(cmd, shell=True, env=os.environ)
            
            if result.returncode == 0:
                # 安装成功，继续下一个包
                pkg_idx += 1
            else:
                # kurulum basarisiz, 尝试下一个镜像
                print(f"[BASARISIZ] {pkg_display} 在 {mirror_name} 安装失败")
                
                # 切换到下一个镜像
                current_mirror_idx += 1
                
                if current_mirror_idx >= len(mirrors_to_try):
                    # Tum kaynaklar basarisiz oldu
                    raise RuntimeError(f"Kurulamadi: {pkg_display}, tum kaynaklar basarisiz")
                
                next_mirror = mirrors_to_try[current_mirror_idx]
                next_mirror_name = urllib.parse.urlparse(next_mirror).hostname or next_mirror
                print(f"[重试] 切换到镜像 {next_mirror_name}，从 {pkg_display} 重新开始...")
                # 不增加 pkg_idx，从当前失败的包重试
                
        except Exception as e:
            print(f"[错误] Kuruluyor: {pkg_display} 时出错: {e}")
            
            # 切换到下一个镜像
            current_mirror_idx += 1
            
            if current_mirror_idx >= len(mirrors_to_try):
                raise RuntimeError(f"Kurulamadi: {pkg_display}, tum kaynaklar basarisiz。错误: {e}")
            
            next_mirror = mirrors_to_try[current_mirror_idx]
            next_mirror_name = urllib.parse.urlparse(next_mirror).hostname or next_mirror
            print(f"[重试] 切换到镜像 {next_mirror_name}，从 {pkg_display} 重新开始...")
    
    print(f"[TAMAM] {desc or requirements_file} kurulumu tamamlandi")


def ensure_git_safe_directory():
    """确保当前目录在 Git safe.directory 列表中，解决所有权问题"""
    try:
        # 将项目根目录添加到 Git safe.directory
        subprocess.run(
            [git, 'config', '--global', '--add', 'safe.directory', str(PATH_ROOT)],
            capture_output=True,
            check=False
        )
    except Exception:
        pass  # 忽略错误，不影响后续操作


def commit_hash():
    """获取当前Git commit hash"""
    global stored_commit_hash
    if stored_commit_hash is not None:
        return stored_commit_hash

    ensure_git_safe_directory()  # 确保 safe.directory 已配置
    try:
        stored_commit_hash = run(f"{git} rev-parse HEAD").strip()
    except Exception:
        stored_commit_hash = "<none>"

    return stored_commit_hash


def restart():
    """重启应用"""
    print('正在重启应用...\n')
    os.execv(sys.executable, ['python'] + sys.argv)


def detect_gpu():
    """检测GPU类型 - 使用多种方法以提高兼容性"""
    
    def check_gpu_keywords(output):
        """检查输出中的GPU关键词，返回 (GPU类型, 显卡名称)"""
        if not output:
            return None, None
        output_upper = output.upper()
        
        # 提取显卡名称（取第一行非空的）
        gpu_name = ""
        for line in output.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('NAME') and not line.startswith('---'):
                gpu_name = line
                break
        
        if any(keyword in output_upper for keyword in ["NVIDIA", "GEFORCE", "GTX", "RTX", "QUADRO", "TESLA"]):
            return "NVIDIA", gpu_name
        elif any(keyword in output_upper for keyword in ["AMD", "RADEON", "ATI"]):
            return "AMD", gpu_name
        elif "INTEL" in output_upper and any(keyword in output_upper for keyword in ["HD GRAPHICS", "UHD GRAPHICS", "IRIS", "ARC"]):
            return "Intel", gpu_name
        return None, None
    
    def check_nvidia_cuda_version():
        """检查 NVIDIA CUDA 驱动版本"""
        try:
            # 尝试运行 nvidia-smi 获取驱动版本
            cmd = 'nvidia-smi --query-gpu=driver_version --format=csv,noheader'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='gbk', errors='ignore')
            driver_version = output.strip().split('\n')[0].strip()
            
            # 尝试从nvidia-smi直接输出获取CUDA版本
            # nvidia-smi输出的第一行通常包含CUDA版本信息
            try:
                cmd_full = 'nvidia-smi'
                full_output = subprocess.check_output(cmd_full, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='gbk', errors='ignore')
                # 解析 "CUDA Version: X.Y" 格式
                import re
                cuda_match = re.search(r'CUDA Version:\s*(\d+\.\d+)', full_output)
                if cuda_match:
                    cuda_version = cuda_match.group(1)
                    cuda_major = int(cuda_version.split('.')[0])
                    return cuda_major, cuda_version, driver_version
            except:
                pass
            
            # 如果无法获取CUDA版本，返回驱动版本
            return None, None, driver_version
        except Exception:
            return None, None, None
    
    try:
        if sys.platform == 'win32':
            # Windows 系统：尝试多种检测方式（优先使用无需安装的方法）
            
            # 方法1: 尝试 PowerShell Get-CimInstance（Windows 8+，无需额外工具）
            try:
                cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"'
                output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='gbk', errors='ignore')
                gpu_type, gpu_name = check_gpu_keywords(output)
                if gpu_type:
                    # 如果是 NVIDIA，检查 CUDA surumu
                    if gpu_type == "NVIDIA":
                        cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                        return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                    return gpu_type, gpu_name, None, None, None
            except Exception:
                pass
            
            # 方法2: 尝试 wmic（经典方法，兼容老系统）
            try:
                cmd = 'wmic path win32_VideoController get name'
                output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='gbk', errors='ignore')
                gpu_type, gpu_name = check_gpu_keywords(output)
                if gpu_type:
                    # 如果是 NVIDIA，检查 CUDA surumu
                    if gpu_type == "NVIDIA":
                        cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                        return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                    return gpu_type, gpu_name, None, None, None
            except Exception:
                pass
            
            # 方法3: 尝试 PowerShell Get-WmiObject（更老的 PowerShell）
            try:
                cmd = 'powershell -NoProfile -Command "Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty Name"'
                output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='gbk', errors='ignore')
                gpu_type, gpu_name = check_gpu_keywords(output)
                if gpu_type:
                    # 如果是 NVIDIA，检查 CUDA surumu
                    if gpu_type == "NVIDIA":
                        cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                        return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                    return gpu_type, gpu_name, None, None, None
            except Exception:
                pass
            
            # 方法4: 尝试读取注册表（最底层的方法）
            try:
                cmd = 'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000" /v DriverDesc'
                output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='gbk', errors='ignore')
                gpu_type, gpu_name = check_gpu_keywords(output)
                if gpu_type:
                    # 如果是 NVIDIA，检查 CUDA surumu
                    if gpu_type == "NVIDIA":
                        cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                        return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                    return gpu_type, gpu_name, None, None, None
            except Exception:
                pass
            
            # 方法5: 尝试使用 wmi Python 库（需要额外安装，作为最后备选）
            try:
                # 先尝试导入，如果失败则尝试安装
                try:
                    import wmi
                except ImportError:
                    # 库不存在，尝试安装
                    try:
                        import subprocess as sp
                        print('Kuruluyor: wmi 库以进行显卡检测...')
                        sp.run([python, '-m', 'pip', 'install', 'wmi', '--quiet'], check=True, timeout=30)
                        import wmi
                        print('wmi kutuphanesi kuruldu')
                    except Exception:
                        # kurulum basarisiz, 跳过
                        raise ImportError('wmi 库安装失败')
                
                # 使用 wmi 检测
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    gpu_type, gpu_name = check_gpu_keywords(gpu.Name)
                    if gpu_type:
                        # 如果是 NVIDIA，检查 CUDA surumu
                        if gpu_type == "NVIDIA":
                            cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                            return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                        return gpu_type, gpu_name, None, None, None
            except (ImportError, Exception):
                pass
                
        else:
            # macOS: 特殊处理 Apple Silicon
            if sys.platform == 'darwin':
                try:
                    # 检测是否是 Apple Silicon (M1/M2/M3/M4 等)
                    import platform
                    machine = platform.machine()
                    
                    if machine == 'arm64':
                        # Apple Silicon Mac，使用 system_profiler 获取芯片信息
                        try:
                            output = subprocess.check_output(
                                "system_profiler SPHardwareDataType | grep 'Chip'",
                                shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5
                            )
                            # 解析芯片名称，例如 "Chip: Apple M4 Pro"
                            chip_name = ""
                            for line in output.strip().split('\n'):
                                if 'Chip' in line:
                                    parts = line.split(':')
                                    if len(parts) >= 2:
                                        chip_name = parts[1].strip()
                                        break
                            
                            if chip_name and ('M1' in chip_name or 'M2' in chip_name or 
                                              'M3' in chip_name or 'M4' in chip_name or
                                              'Apple' in chip_name):
                                # Apple Silicon，支持 Metal
                                return "AppleSilicon", chip_name, None, None, None
                        except Exception:
                            pass
                        
                        # 如果无法获取具体芯片名称，但确定是 arm64，仍然返回 Apple Silicon
                        return "AppleSilicon", "Apple Silicon", None, None, None
                    
                    # Intel Mac，继续使用下面的通用检测逻辑
                except Exception:
                    pass
            
            # Linux 或 Intel Mac: 使用lspci或其他工具
            try:
                output = subprocess.check_output("lspci | grep -i vga", shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='utf-8', errors='ignore')
                gpu_type, gpu_name = check_gpu_keywords(output)
                if gpu_type:
                    # 如果是 NVIDIA，检查 CUDA surumu
                    if gpu_type == "NVIDIA":
                        cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                        return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                    return gpu_type, gpu_name, None, None, None
            except:
                pass
            
            # 尝试使用 lshw (Linux only)
            try:
                output = subprocess.check_output("lshw -C display 2>/dev/null | grep 'product:'", shell=True, text=True, stderr=subprocess.DEVNULL, timeout=5, encoding='utf-8', errors='ignore')
                gpu_type, gpu_name = check_gpu_keywords(output)
                if gpu_type:
                    # 如果是 NVIDIA，检查 CUDA surumu
                    if gpu_type == "NVIDIA":
                        cuda_major, cuda_version, driver_version = check_nvidia_cuda_version()
                        return gpu_type, gpu_name, cuda_major, cuda_version, driver_version
                    return gpu_type, gpu_name, None, None, None
            except:
                pass
                
    except Exception:
        pass
    
    return "CPU", "", None, None, None


def detect_amd_gfx_version(gpu_name):
    """根据 AMD 显卡名称检测对应的 gfx surumu
    
    返回: (gfx_version, architecture_name, has_torch_support) 或 (None, None, False)
    """
    if not gpu_name:
        return None, None, False
    
    gpu_name_upper = gpu_name.upper()
    
    # AMD 显卡型号到 gfx surumu的映射（Windows ROCm 7.2 + PyTorch 支持列表）
    amd_gpu_mapping = {
        # CDNA 数据中心系列 - 支持
        'gfx94X-dcgpu': {
            'keywords': ['MI300A', 'MI300X'],
            'name': 'CDNA (MI300A/MI300X)',
            'has_torch': True
        },
        'gfx950-dcgpu': {
            'keywords': ['MI350X', 'MI355X'],
            'name': 'CDNA (MI350X/MI355X)',
            'has_torch': True
        },

        # RDNA 3 架构 - 支持的具体型号
        'gfx110X-dgpu': {
            'keywords': ['RX 7900 XTX', '7900 XTX', 'RX 7800 XT', '7800 XT', 'RX 7700S', '7700S', 'FRAMEWORK LAPTOP 16'],
            'name': 'RDNA 3 (RX 7900 XTX / RX 7800 XT / RX 7700S)',
            'has_torch': True
        },

        # Strix Halo iGPU - 支持
        'gfx1151': {
            'keywords': ['STRIX HALO'],
            'name': 'Strix Halo iGPU',
            'has_torch': True
        },

        # RDNA 4 架构 - 支持的具体型号
        'gfx120X-all': {
            'keywords': ['RX 9060 XT', 'RX 9060', 'RX 9070 XT', 'RX 9070'],
            'name': 'RDNA 4 (RX 9060/9070 系列)',
            'has_torch': True
        },
        
        # 以下架构不支持 torch（已验证）
        # RDNA 2 架构 (RX 6000 系列) - 不支持
        'gfx103X-dgpu': {
            'keywords': ['RX 6', '6900', '6800', '6700', '6600', '6500', '6400'],
            'name': 'RDNA 2 (RX 6000 系列) - 不支持 PyTorch',
            'has_torch': False
        },
        
        # RDNA 1 架构 (RX 5000 系列) - 不支持
        'gfx101X-dgpu': {
            'keywords': ['RX 5', '5700', '5600', '5500'],
            'name': 'RDNA 1 (RX 5000 系列) - 不支持 PyTorch',
            'has_torch': False
        },
        
        # Vega 架构 - 不支持
        'gfx90X-dcgpu': {
            'keywords': ['VEGA', 'RADEON VII', 'MI25', 'MI50', 'MI60'],
            'name': 'Vega (Radeon VII / MI50/60) - 不支持 PyTorch',
            'has_torch': False
        },
    }
    
    # 尝试匹配
    for gfx_version, info in amd_gpu_mapping.items():
        for keyword in info['keywords']:
            if keyword in gpu_name_upper:
                return gfx_version, info['name'], info.get('has_torch', False)
    
    return None, None, False


def print_supported_amd_gpu_types():
    """打印当前支持的 AMD 显卡类型"""
    print('Desteklenen AMD ekran karti turleri:')
    print('  - MI300A / MI300X (gfx94X-dcgpu)')
    print('  - MI350X / MI355X (gfx950-dcgpu)')
    print('  - RX 7900 XTX / RX 7800 XT / RX 7700S (Framework Laptop 16) (gfx110X-dgpu)')
    print('  - AMD Strix Halo iGPU (gfx1151)')
    print('  - RX 9060 / RX 9060 XT / RX 9070 / RX 9070 XT (gfx120X-all)')
    print('  ⚠️  Windows 版 ROCm 7.2 PyTorch 需要 AMD 显卡驱动 26.1.1')


def choose_when_amd_unsupported():
    """AMD 不支持时给用户选择，默认 CPU"""
    print('')
    print('⚠️  当前显卡不在 AMD ROCm PyTorch 支持列表中。')
    print_supported_amd_gpu_types()
    print('')
    print('Seciniz:')
    print('  [1] CPU surumu kullan (varsayilan, onerilen)')
    print('  [2] AMD surumunu zorla kur (deneysel, basarisiz olabilir)')
    print('  [3] Kurulumdan cik')
    print('')

    while True:
        choice = input('Seciniz (1/2/3, varsayilan 1): ').strip()
        if choice in ['', '1']:
            return 'cpu'
        elif choice == '2':
            return 'force_amd'
        elif choice == '3':
            return 'exit'
        else:
            print('Gecersiz giris, lutfen 1, 2 veya 3 girin')


def detect_installed_pytorch_version():
    """检测当前安装的PyTorch版本类型(CPU/GPU/Metal)"""
    try:
        # 在子进程中检测，避免在主进程中加载 torch DLL
        # 这样可以在需要时Kaldiriliyor: torch
        code = """
import sys
try:
    import torch
    # 检查 AMD ROCm
    if hasattr(torch.version, 'hip') and torch.version.hip:
        print(f"AMD|ROCm {torch.version.hip}")
    # 检查 NVIDIA CUDA
    elif torch.cuda.is_available():
        cuda_version = torch.version.cuda
        if cuda_version:
            print(f"GPU|CUDA {cuda_version}")
        else:
            print("GPU|Unknown CUDA")
    # 检查 Apple Silicon Metal (MPS)
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        print("Metal|MPS")
    else:
        print("CPU|CPU-only")
except (ImportError, AttributeError):
    print("None|未安装")
except OSError as e:
    print(f"None|安装损坏: {e}")
"""
        result = subprocess.run(
            [python, '-c', code],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if '|' in output:
                pytorch_type, detail = output.split('|', 1)
                return pytorch_type, detail
        
        return None, "检测失败"
    except Exception:
        return None, "检测失败"


def get_requirements_file_from_env():
    """从当前虚拟环境检测应该使用哪个requirements文件"""
    pytorch_type, detail = detect_installed_pytorch_version()
    
    if pytorch_type == "GPU":
        return 'requirements_gpu.txt', pytorch_type, detail
    elif pytorch_type == "Metal":
        return 'requirements_metal.txt', pytorch_type, detail
    elif pytorch_type == "AMD":
        return 'requirements_amd.txt', pytorch_type, detail
    elif pytorch_type == "CPU":
        return 'requirements_cpu.txt', pytorch_type, detail
    else:
        # 未安装PyTorch,返回None让后续逻辑自动检测
        return None, None, detail


def prepare_environment(args):
    """准备运行环境
    
    返回: (use_amd_pytorch, amd_gfx_version) - 是否使用AMD PyTorch及其gfx版本
    """
    
    if args.frozen:
        print('frozen modu: bagimlilik kurulumu atlaniyor')
        return False, None

    # 确保 packaging 已Kuruluyor: (需要 < 25.0 surumu)
    try:
        import packaging
        import packaging.version
        import packaging.utils
        # 检查是否有 packaging.requirements (在 25.0 中已移除)
        try:
            from packaging.requirements import Requirement
        except (ImportError, AttributeError):
            # packaging surumu过高,需要降级
            print('Uyumsuz packaging surumu tespit edildi, uyumlu surum kuruluyor...')
            run_pip("install 'packaging<25.0'", "packaging")
            import packaging
            import packaging.version
            import packaging.utils
            print('✓ packaging kuruldu')
    except (ModuleNotFoundError, ImportError):
        print('Kuruluyor: packaging 模块...')
        run_pip("install 'packaging<25.0'", "packaging")
        try:
            import packaging
            import packaging.version
            import packaging.utils
            print('✓ packaging kuruldu')
        except (ModuleNotFoundError, ImportError):
            print('✗ Uyari: packaging kurulamadi')

    print('\n正在检查依赖...\n')
    
    # 将 packaging 目录添加到 Python 路径，以便导入 build_utils
    packaging_dir = PATH_ROOT / 'packaging'
    if str(packaging_dir) not in sys.path:
        sys.path.insert(0, str(packaging_dir))
    
    # 导入依赖检查工具
    try:
        from build_utils.package_checker import check_req_file
        print('✓ Bagimlilik kontrol araci yuklendi')
    except ImportError as e:
        print(f'✗ Uyari: Bagimlilik kontrol araci yuklenemedi')
        print(f'   Neden: {e}')
        print('   Artimsal kontrol atlaniyor, tum bagimliliklar yeniden kurulacak')
        check_req_file = lambda x: False

    # 检测GPU并选择对应的依赖文件
    gpu_type, gpu_name, cuda_major, cuda_version, driver_version = detect_gpu()
    print(f'\n检测到的计算设备: {gpu_type}')
    if gpu_name:
        print(f'Ekran karti: {gpu_name}')
    if cuda_version:
        print(f'CUDA Surum: {cuda_version}')
        if driver_version:
            print(f'驱动Surum: {driver_version}')
    print()
    
    # 根据GPU类型选择requirements文件
    use_amd_pytorch = False  # 初始化AMD PyTorch标志
    amd_gfx_version = None    # 初始化gfx版本
    
    if args.requirements != 'auto':
        # 用户手动指定,尊重用户选择
        requirements_file = args.requirements
        # 如果手动指定了 requirements_amd.txt，需要检测 gfx surumu并Kuruluyor: AMD PyTorch
        if requirements_file == 'requirements_amd.txt':
            use_amd_pytorch = True
            detected_installed_amd = False
            # 尝试从环境中检测已安装的 AMD PyTorch surumu（在子进程中检测）
            try:
                code = """
import sys
try:
    import torch
    if hasattr(torch.version, 'hip') and torch.version.hip:
        print(f"installed|{torch.version.hip}")
    else:
        print("not_amd|")
except:
    print("not_installed|")
"""
                result = subprocess.run(
                    [python, '-c', code],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding='utf-8',
                    errors='ignore'
                )
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    if output.startswith('installed|'):
                        detected_installed_amd = True
                        rocm_version = output.split('|')[1]
                        # 已Kuruluyor: AMD ROCm PyTorch，获取版本信息
                        print(f'\n检测到已Kuruluyor: AMD ROCm PyTorch')
                        print(f'ROCm Surum: {rocm_version}')
                        print('')
                        
                        # 询问是否更新
                        update_choice = input('AMD ROCm PyTorch guncelleme? (y/n, varsayilan n): ').strip().lower()
                        if update_choice in ['y', 'yes']:
                            # 自动检测 gfx surumu
                            detected_gfx, arch_name, has_torch = detect_amd_gfx_version(gpu_name) if gpu_name else (None, None, False)
                            
                            if detected_gfx and has_torch:
                                print(f'\n自动识别架构: {arch_name}')
                                print(f'对应 gfx Surum: {detected_gfx}')
                                print('✓ Otomatik tespit edilen gfx surumu kullaniliyor')
                                amd_gfx_version = detected_gfx
                            elif detected_gfx and not has_torch:
                                print(f'\n⚠️  警告: {detected_gfx} AMD ROCm PyTorch desteklemiyor')
                                user_action = choose_when_amd_unsupported()
                                if user_action == 'exit':
                                    print('Kurulum iptal edildi, ekran karti ve surucu surumunu dogrulayin.')
                                    sys.exit(0)
                                elif user_action == 'force_amd':
                                    print('⚠️  AMD surumunu zorla kur secildi, uyumluluk garantisi yoktur.')
                                    use_amd_pytorch = True
                                    amd_gfx_version = detected_gfx
                                else:
                                    requirements_file = 'requirements_cpu.txt'
                                    use_amd_pytorch = False
                            else:
                                print('\n⚠️  无法自动检测到受支持的 AMD gfx surumu')
                                user_action = choose_when_amd_unsupported()
                                if user_action == 'exit':
                                    print('Kurulum iptal edildi, ekran karti ve surucu surumunu dogrulayin.')
                                    sys.exit(0)
                                elif user_action == 'force_amd':
                                    print('⚠️  AMD surumunu zorla kur secildi, uyumluluk garantisi yoktur.')
                                    use_amd_pytorch = True
                                else:
                                    requirements_file = 'requirements_cpu.txt'
                                    use_amd_pytorch = False
                        else:
                            use_amd_pytorch = False
            except Exception:
                # 检测失败，继续
                pass
            
            if not use_amd_pytorch:
                # 未安装或非 AMD PyTorch
                if requirements_file == 'requirements_amd.txt':
                    if detected_installed_amd:
                        print('\n检测到已Kuruluyor: AMD ROCm PyTorch，本次不更新。')
                    else:
                        print('\n未检测到 AMD ROCm PyTorch')
                        print('[BILGI] requirements_amd.txt manuel belirlendi ancak AMD PyTorch kurulu degil')
                        print('[BILGI] AMD PyTorch kurmak icin Adim1-IlkKurulum.bat calistirin')
                else:
                    print(f'\n✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                use_amd_pytorch = False
        else:
            pass  # 不是AMD，use_amd_pytorch已在开头初始化为False
    else:
        # 自动选择
        if gpu_type == "NVIDIA":
            print('=' * 50)
            print('NVIDIA GPU tespit edildi')
            print('=' * 50)
            print('')
            
            # 检查 CUDA surumu
            if cuda_major is not None:
                if cuda_major < 12:
                    print('⚠️  Uyari: CUDA surumu 12 nin altinda tespit edildi')
                    print(f'   当前 CUDA Surum: {cuda_version}')
                    print(f'   GPU surumu gerekliligi: CUDA 12.x')
                    print(f'   Surucu surumu gerekliligi: >= 525.60.13')
                    print('')
                    print('CUDA surumunuz cok dusuk, GPU surumunu kullanamazsiniz.')
                    print('Seciniz:')
                    print('  [1] NVIDIA surucu guncelleyip kurulumu yeniden calistirin')
                    print('  [2] CPU surumunu kullanin')
                    print('')
                    
                    while True:
                        choice = input('Seciniz (1/2, varsayilan 2): ').strip()
                        if choice == '1':
                            print('\nEn son surucu icin NVIDIA resmi sitesini ziyaret edin:')
                            print('https://www.nvidia.com/Download/index.aspx')
                            print('\nSurucu kurulumundan sonra bu betigi yeniden calistirin')
                            sys.exit(0)
                        elif choice in ['', '2']:
                            requirements_file = 'requirements_cpu.txt'
                            print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                            break
                        else:
                            print('Gecersiz giris, lutfen 1 veya 2 girin')
                else:
                    # CUDA surumu符合要求
                    print('GPU surumu gereklilikleri:')
                    print('  - CUDA 12.x destekleyen NVIDIA ekran karti')
                    print('  - Ekran karti surucu surumu >= 525.60.13')
                    print('')
                    print(f'✓ CUDA surumunuz {cuda_version} gereklilikleri karsilaniyor')
                    print('')
                    print('Emin degilseniz CPU surumunu secin (daha yavas ama daha uyumlu)')
                    print('')
                    
                    while True:
                        choice = input('GPU surumu kullanilsin? (y/n, varsayilan y): ').strip().lower()
                        if choice in ['', 'y', 'yes']:
                            requirements_file = 'requirements_gpu.txt'
                            print(f'✓ Kullaniliyor: {requirements_file} (NVIDIA CUDA)')
                            break
                        elif choice in ['n', 'no']:
                            requirements_file = 'requirements_cpu.txt'
                            print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                            break
                        else:
                            print('无效输入,请输入 y 或 n')
            else:
                # 无法检测 CUDA surumu
                print('⚠️  CUDA surumu tespit edilemiyor (nvidia-smi kurulu olmayabilir)')
                print('')
                print('GPU surumu gereklilikleri:')
                print('  - CUDA 12.x destekleyen NVIDIA ekran karti')
                print('  - Ekran karti surucu surumu >= 525.60.13')
                print('')
                print('Emin degilseniz CPU surumunu secin (daha yavas ama daha uyumlu)')
                print('')
                
                while True:
                    choice = input('GPU surumu kullanilsin? (y/n, varsayilan y): ').strip().lower()
                    if choice in ['', 'y', 'yes']:
                        requirements_file = 'requirements_gpu.txt'
                        print(f'✓ Kullaniliyor: {requirements_file} (NVIDIA CUDA)')
                        break
                    elif choice in ['n', 'no']:
                        requirements_file = 'requirements_cpu.txt'
                        print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                        break
                    else:
                        print('无效输入,请输入 y 或 n')
                    
        elif gpu_type == "AMD":
            # 检测 AMD GPU 的 gfx surumu
            detected_gfx, arch_name, has_torch = detect_amd_gfx_version(gpu_name)
            
            print('=' * 50)
            print('AMD GPU tespit edildi')
            print('=' * 50)
            print('')
            
            if detected_gfx:
                print(f'自动识别架构: {arch_name}')
                print(f'对应 gfx Surum: {detected_gfx}')
                if not has_torch:
                    print(f'⚠️  Bu ekran karti AMD ROCm PyTorch desteklemiyor')
                    print(f'⚠️  CPU surumu onerilir')
            else:
                print('⚠️  AMD GPU mimarisi otomatik taninamadi')
            
            print('')
            print('AMD GPU destek secenekleri:')
            print('  [1] AMD ROCm GPU surumu (deneysel, uyumlu AMD ekran karti gerektirir)')
            print('  [2] CPU surumu (onerilen, uyumlu)')
            print('  ⚠️ Windows ROCm 7.2 PyTorch, AMD ekran karti surucu 26.1.1 gerektirir')
            print('')
            
            if detected_gfx and has_torch:
                print(f'Oneri: [1] seciniz ve tespit edilen {detected_gfx}')
            else:
                print('Oneri: [2] CPU surumunu seciniz')
            print('')

            # 检测到不支持时：展示支持型号并给出选择（默认 CPU）
            if not (detected_gfx and has_torch):
                user_action = choose_when_amd_unsupported()
                if user_action == 'exit':
                    print('Kurulum iptal edildi, ekran karti ve surucu surumunu dogrulayin.')
                    sys.exit(0)
                elif user_action == 'force_amd':
                    requirements_file = 'requirements_amd.txt'
                    use_amd_pytorch = True
                    amd_gfx_version = detected_gfx
                    print('⚠️  AMD surumunu zorla kur secildi, uyumluluk garantisi yoktur.')
                    print(f'✓ Kullaniliyor: {requirements_file} (AMD 强制安装)')
                else:
                    requirements_file = 'requirements_cpu.txt'
                    use_amd_pytorch = False
                    print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
            else:
                while True:
                    choice = input('Seciniz (1/2, varsayilan 2): ').strip()
                    if choice == '1':
                        amd_gfx_version = detected_gfx
                        requirements_file = 'requirements_amd.txt'  # 使用专用的 AMD 依赖文件
                        use_amd_pytorch = True
                        print(f'✓ Otomatik taninan ve kullanilan: {amd_gfx_version}')
                        print(f'✓ AMD ROCm PyTorch kullanilacak ({amd_gfx_version})')
                        print(f'✓ Bagimlilik dosyasi: {requirements_file}')
                        break
                    elif choice in ['', '2']:
                        requirements_file = 'requirements_cpu.txt'
                        print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                        break
                    else:
                        print('Gecersiz giris, lutfen 1 veya 2 girin')
                    
        elif gpu_type == "AppleSilicon":
            # Apple Silicon Mac，使用 Metal 加速
            print('=' * 50)
            print('Apple Silicon tespit edildi')
            print('=' * 50)
            print('')
            if gpu_name:
                print(f'芯片型号: {gpu_name}')
            print('')
            print('✓ Apple Silicon Metal hizlandirmasini destekliyor')
            print('✓ En iyi performans icin Metal surumu kullanilacak')
            print('')
            requirements_file = 'requirements_metal.txt'
            print(f'✓ Kullaniliyor: {requirements_file} (Apple Metal)')
                    
        elif gpu_type == "CPU":
            # 自动检测失败,让用户手动选择
            print('=' * 50)
            print('⚠️  Ekran karti turu otomatik tespit edilemiyor')
            print('=' * 50)
            print('')
            print('请手动选择安装版本:')
            print('  [1] NVIDIA GPU surumu (CUDA) - NVIDIA ekran karti gerektirir')
            print('  [2] AMD GPU surumu (ROCm) - uyumlu AMD ekran karti gerektirir')
            print('  [3] CPU surumu - tum bilgisayarlarla uyumlu')
            print('')
            
            while True:
                choice = input('Seciniz (1/2/3, varsayilan 3): ').strip()
                if choice == '1':
                    requirements_file = 'requirements_gpu.txt'
                    print(f'✓ Kullaniliyor: {requirements_file} (NVIDIA CUDA)')
                    break
                elif choice == '2':
                    # AMD GPU（纯自动检测）
                    print('')
                    print('✓ PyTorch destekleyen AMD gfx surumleri:')
                    print('  - gfx94X-dcgpu: MI300A / MI300X')
                    print('  - gfx950-dcgpu: MI350X / MI355X')
                    print('  - gfx110X-dgpu: RX 7900 XTX / RX 7800 XT / RX 7700S (Framework Laptop 16)')
                    print('  - gfx1151:      AMD Strix Halo iGPU')
                    print('  - gfx120X-all:  RX 9060 / RX 9060 XT / RX 9070 / RX 9070 XT')
                    print('')
                    print('✗ PyTorch desteklemeyen surum:')
                    print('  - gfx101X-dgpu: RX 5000 系列')
                    print('  - gfx103X-dgpu: RX 6000 系列')
                    print('  - gfx90X-dcgpu: Vega / Radeon VII')
                    print('')

                    detected_gfx, arch_name, has_torch = detect_amd_gfx_version(gpu_name) if gpu_name else (None, None, False)
                    if detected_gfx and has_torch:
                        amd_gfx_version = detected_gfx
                        requirements_file = 'requirements_amd.txt'
                        use_amd_pytorch = True
                        print(f'✓ 自动识别架构: {arch_name}')
                        print(f'✓ AMD ROCm PyTorch kullanilacak ({amd_gfx_version})')
                        print(f'✓ Bagimlilik dosyasi: {requirements_file}')
                        break
                    else:
                        user_action = choose_when_amd_unsupported()
                        if user_action == 'exit':
                            print('Kurulum iptal edildi, ekran karti ve surucu surumunu dogrulayin.')
                            sys.exit(0)
                        elif user_action == 'force_amd':
                            requirements_file = 'requirements_amd.txt'
                            use_amd_pytorch = True
                            amd_gfx_version = detected_gfx
                            print('⚠️  AMD surumunu zorla kur secildi, uyumluluk garantisi yoktur.')
                            print(f'✓ Kullaniliyor: {requirements_file} (AMD 强制安装)')
                        else:
                            requirements_file = 'requirements_cpu.txt'
                            use_amd_pytorch = False
                            print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                        break
                elif choice in ['', '3']:
                    requirements_file = 'requirements_cpu.txt'
                    print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                    break
                else:
                    print('Gecersiz giris, lutfen 1, 2 veya 3 girin')
                    
        else:
            # Intel GPU - 在 Windows 上支持有限,推荐使用 CPU surumu
            print('=' * 50)
            print('Intel GPU tespit edildi')
            print('=' * 50)
            print('')
            print('⚠️  Intel GPU PyTorch destegi sinirli')
            print('En iyi uyumluluk icin CPU surumu onerilir')
            print('')
            print('Seciniz:')
            print('  [1] NVIDIA GPU surumu (ayri ekran karti varsa)')
            print('  [2] CPU surumu (onerilen)')
            print('')
            
            while True:
                choice = input('Seciniz (1/2, varsayilan 2): ').strip()
                if choice == '1':
                    requirements_file = 'requirements_gpu.txt'
                    print(f'✓ Kullaniliyor: {requirements_file} (NVIDIA CUDA)')
                    break
                elif choice in ['', '2']:
                    requirements_file = 'requirements_cpu.txt'
                    print(f'✓ Kullaniliyor: {requirements_file} (CPU surumu)')
                    break
                else:
                    print('Gecersiz giris, lutfen 1 veya 2 girin')
    
    # 选择对应的PyTorch版本 (根据requirements_gpu.txt中的版本)
    # 注意: 不再单独Kuruluyor: PyTorch，而是通过 requirements 文件统一安装
    # 这样可以避免版本冲突和 DLL 损坏问题
    
    # 检查是否需要卸载不匹配的 PyTorch surumu
    need_reinstall = args.reinstall_torch
    
    if not need_reinstall:
        # 检测当前安装的 PyTorch 类型
        installed_pytorch_type, installed_detail = detect_installed_pytorch_version()
        target_type = "GPU" if "gpu" in requirements_file.lower() else "CPU"
        
        if installed_pytorch_type is not None and installed_pytorch_type != target_type:
            print('\n' + '=' * 50)
            print('⚠️  警告: 检测到 PyTorch surumu不匹配')
            print('=' * 50)
            print(f'Mevcut kurulum: {installed_pytorch_type} surumu ({installed_detail})')
            print(f'目标Surum: {target_type} surumu')
            print('')
            print('Farkli PyTorch surumleri DLL catismasi ve yukleme hatasina yol acar')
            print('Eski surumu kaldirip yeniden kurmaniz onerilir')
            print('')
            need_reinstall = True
    
    # 如果需要重装 PyTorch，先卸载
    if need_reinstall or use_amd_pytorch:
        print('Mevcut PyTorch kaldiriliyor...')
        print('[IPUCU] Baska Python isleminin calismadigindan emin olun')
        
        # 尝试多次卸载，处理文件占用问题
        max_retries = 3
        for retry in range(max_retries):
            try:
                run(f'"{python}" -m pip uninstall torch torchvision torchaudio -y', "Kaldiriliyor: PyTorch", "无法Kaldiriliyor: PyTorch", live=True)
                break
            except Exception as e:
                if retry < max_retries - 1:
                    print(f'卸载失败（尝试 {retry + 1}/{max_retries}），可能有文件被占用')
                    print('请关闭所有使用 PyTorch 的程序，然后按回车继续...')
                    input()
                else:
                    print(f'Uyari: PyTorch kaldirilamadi, zorla uzerine kurulmaya calisilacak')
                    print(f'错误: {e}')
        
        # 强制清理 pip 缓存，避免使用缓存的错误版本
        print('pip onbellegi temizleniyor...')
        try:
            run(f'"{python}" -m pip cache purge', "Onbellek temizleniyor", "无法Onbellek temizleniyor")
        except:
            pass
    
    # 如果用户选择了 AMD ROCm PyTorch，先安装它
    if use_amd_pytorch:
        print('\n' + '=' * 50)
        print('AMD ROCm PyTorch kuruluyor')
        print('=' * 50)
        if amd_gfx_version:
            print(f'gfx Surum: {amd_gfx_version}')
        print('Mod: ROCm SDK 7.2 sabit URL kurulumu')
        print('⚠️  On kosul: Windows ROCm 7.2 PyTorch, AMD ekran karti surucu 26.1.1 gerektirir')
        print('')

        # 第1步：先Kuruluyor: ROCm SDK 依赖
        rocm_sdk_urls = [
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl",
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl",
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl",
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm-7.2.0.dev0.tar.gz",
        ]

        # 第2步：再Kuruluyor: PyTorch 三件套
        rocm_torch_urls = [
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl",
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchaudio-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl",
            "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchvision-0.24.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl",
        ]

        sdk_urls_str = " ".join([f'"{u}"' for u in rocm_sdk_urls])
        torch_urls_str = " ".join([f'"{u}"' for u in rocm_torch_urls])
        install_sdk_cmd = f'"{python}" -m pip install --no-cache-dir {sdk_urls_str}'
        install_torch_cmd = f'"{python}" -m pip install --no-cache-dir {torch_urls_str}'

        try:
            run(install_sdk_cmd, "Adim 1/2: AMD ROCm SDK bagimliliklerini kur", "AMD ROCm SDK bagimlilikleri kurulamadi", live=True)
            run(install_torch_cmd, "Adim 2/2: AMD ROCm PyTorch kur", "AMD ROCm PyTorch kurulamadi", live=True)
            print('\n✓ AMD ROCm PyTorch kurulumu tamamlandi')
            print('\n⚠️  注意:')
            print('  - AMD ROCm PyTorch deneysel bir ozellik')
            print('  - Ilk calistirmada bazi islemler derlenebilir')
            print('  - Sorun yasarsaniz CPU surumunu kullanin')
        except Exception as e:
            print(f'\n✗ AMD ROCm PyTorch kurulamadi: {e}')
            print('\n建议:')
            print('  1. Ag baglantisini kontrol edin')
            print('  2. Python surumunun 3.12 oldugunu dogrulayin')
            print('  3. Sorun devam ederse CPU surumuyle yeniden kurun')
            # kurulum basarisiz, 返回失败状态
            return False, None

    # 检查并安装其他依赖
    if not os.path.exists(requirements_file):
        print(f'Uyari: Bulunamadi: {requirements_file}')
        return False, None

    print(f'\n正在检查依赖: {requirements_file}')
    if not check_req_file(requirements_file) or need_reinstall:
        if need_reinstall:
            print(f'Tum bagimliliklar zorla yeniden kuruluyor...')
            # 只有 AMD 用户才会在前面单独Kuruluyor: PyTorch，其他用户需要从 requirements 安装
            if use_amd_pytorch:
                print('跳过 requirements 中的 PyTorch（AMD ROCm 已单独安装）')
                # 创建临时 requirements 文件，排除 torch/torchvision/torchaudio
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_req:
                    with open(requirements_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line_stripped = line.strip()
                            # 跳过 torch/torchvision/torchaudio 及其依赖包相关行
                            if line_stripped and not line_stripped.startswith('#'):
                                pkg_name = line_stripped.split('==')[0].split('>=')[0].split('<=')[0].split('<')[0].split('>')[0].split('[')[0].split('@')[0].strip()
                                # 排除 PyTorch 及其生态包（这些包依赖 torch，会触发 torch 安装）
                                pytorch_related = ['torch', 'torchvision', 'torchaudio', 'xformers', 'torchsummary', 'open_clip_torch']
                                if pkg_name.lower() not in pytorch_related:
                                    tmp_req.write(line)
                            else:
                                tmp_req.write(line)
                    tmp_req_path = tmp_req.name
                
                try:
                    run_pip_requirements(tmp_req_path, f"{requirements_file} icindeki bagimliliklar（跳过PyTorch）")
                finally:
                    # 删除临时文件
                    try:
                        os.unlink(tmp_req_path)
                    except:
                        pass
            else:
                run_pip_requirements(requirements_file, f"{requirements_file} icindeki bagimliliklar")
        else:
            print(f'Eksik bagimlilikler bulundu, kuruluyor...')
            # 使用逐个包安装，失败时从失败的包开始切换镜像重试
            run_pip_requirements(requirements_file, f"{requirements_file} icindeki bagimliliklar")
    else:
        print(f'Bagimliliklar karsilandi ✓')
    
    # 返回 AMD PyTorch 相关信息
    return use_amd_pytorch, amd_gfx_version


def update_repository(args):
    """更新代码库"""
    if getattr(sys, 'frozen', False):
        print('打包版本,跳过更新检查')
        return False

    if not args.update:
        return False

    print('Guncellemeler kontrol ediliyor...')
    try:
        current_commit = commit_hash()
        run(f"{git} fetch origin {BRANCH}", desc="正在从远程拉取更新...", errdesc="拉取更新失败")
        latest_commit = run(f"{git} rev-parse origin/{BRANCH}").strip()

        if current_commit != latest_commit:
            print("Yeni surum bulundu, guncelleniyor...")
            run(f"{git} pull origin {BRANCH}", desc="Kod deposu guncelleniyor...", errdesc="更新失败")
            print("Guncelleme tamamlandi, uygulama yeniden baslatiliyor...")
            restart()
            return True
        else:
            print("Zaten en yeni surum")
    except Exception as e:
        print(f"Guncelleme kontrolu basarisiz: {e}")
        print("Mevcut surum kullanilmaya devam ediliyor")
    
    return False


def check_version_info():
    """检查版本信息"""
    ensure_git_safe_directory()  # 确保 safe.directory 已配置
    print()
    print("正在检查版本...")
    print("=" * 40)
    
    # 获取当前版本
    version_file = PATH_ROOT / "packaging" / "VERSION"
    try:
        if version_file.exists():
            current_version = version_file.read_text(encoding='utf-8').strip()
        else:
            current_version = "unknown"
    except Exception:
        current_version = "unknown"
    
    # fetch远程
    try:
        subprocess.run([git, 'fetch', 'origin'], capture_output=True, check=False)
    except Exception:
        pass
    
    # 获取远程版本
    try:
        result = subprocess.run(
            [git, 'show', 'origin/main:packaging/VERSION'],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            remote_version = result.stdout.strip()
        else:
            remote_version = "unknown"
    except Exception:
        remote_version = "unknown"
    
    print(f"Mevcut surum - {current_version}")
    print(f"Uzak surum - {remote_version}")
    
    if current_version == remote_version:
        print()
        print("[BILGI] Zaten en yeni surum")
    elif remote_version == "unknown":
        print()
        print("[UYARI] Uzak surum bilgisi alinamadi")
    else:
        print()
        print("[YENI SURUM BULUNDU]")
    
    print("=" * 40)
    return current_version, remote_version


def update_code_force(skip_confirm=False):
    """强制更新代码（同步到远程）

    Args:
        skip_confirm: 是否跳过确认提示（用于完整更新流程中）
    """
    ensure_git_safe_directory()  # 确保 safe.directory 已配置
    print()
    print("=" * 40)
    print("更新代码 (强制同步)")
    print("=" * 40)
    print()

    if not skip_confirm:
        print("[UYARI] Uzak dala zorla senkronize edilecek, yerel degisiklikler silinecek")
        confirm = input("Guncellemeye devam edilsin mi? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Guncelleme iptal edildi")
            return False
    
    print()
    print("Uzak guncellemeler aliniyor...")
    try:
        subprocess.run([git, 'fetch', 'origin'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[HATA] Uzak guncellemeler alinamadi: {e}")
        return False
    
    print()
    print("Uzak dala zorla senkronize ediliyor...")
    try:
        subprocess.run([git, 'reset', '--hard', 'origin/main'], check=True)
        print("[TAMAM] Kod guncellendi")
        
        # 清理平台特定文件
        import platform
        import os
        
        if platform.system() == 'Windows':
            # Windows 环境清理 macOS 文件
            files_to_remove = [
                'macOS_1_首次安装.sh',
                'macOS_2_启动Qt界面.sh',
                'macOS_3_检查更新并启动.sh',
                'macOS_4_更新维护.sh',
                '.gitattributes',
                '.gitignore',
                'LICENSE.txt'
            ]
            print("[TAMAM] macOS betikleri ve Git yapilandirma dosyalari temizlendi")
        elif platform.system() == 'Darwin':
            # macOS 环境清理 Windows 文件
            files_to_remove = [
                '步骤1-首次安装.bat',
                '步骤2-启动Qt界面.bat',
                '步骤3-检查更新并启动.bat',
                '步骤4-更新维护.bat',
                '.gitattributes',
                '.gitignore',
                'LICENSE.txt'
            ]
            print("[TAMAM] Windows betikleri ve Git yapilandirma dosyalari temizlendi")
        else:
            files_to_remove = []
        
        for file in files_to_remove:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except Exception:
                    pass  # 忽略删除失败
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"[HATA] Kod guncellenemedi: {e}")
        return False


def update_dependencies(args):
    """更新依赖"""
    print()
    print("=" * 40)
    print("Bagimliliklari Guncelle/Kur")
    print("=" * 40)
    print()
    
    # 设置参数，让 prepare_environment 处理所有逻辑
    args.update_deps = True
    args.frozen = False
    args.reinstall_torch = False
    
    # 检测已安装的 PyTorch 类型来决定 requirements 文件
    req_file, pytorch_type, detail = get_requirements_file_from_env()
    if req_file:
        args.requirements = req_file
        print(f"Tespit edilen PyTorch turu: {pytorch_type} ({detail})")
        print(f"Kullaniliyor: {req_file}")
    else:
        args.requirements = 'auto'
        print("PyTorch tespit edilemedi, ilk kurulum yapilacak...")
    
    print()
    
    try:
        prepare_environment(args)
        print()
        print("[TAMAM] Bagimliliklar guncellendi")
        return True
    except Exception as e:
        print(f"[HATA] Bagimliliklar guncellenemedi: {e}")
        return False


def update_dependencies_selective(args, missing_packages):
    """只更新/安装缺失的依赖包
    
    正确处理 PyTorch 相关包需要从专门源下载的逻辑
    安装前会检查包是否已安装，避免重复安装
    """
    import urllib.parse
    
    print()
    print("=" * 40)
    print("Eksik Bagimlilikleri Kur")
    print("=" * 40)
    print()
    
    if not missing_packages:
        print("[BILGI] Eksik bagimlilik yok")
        return True
    
    # 导入依赖检查工具
    packaging_dir = PATH_ROOT / 'packaging'
    if str(packaging_dir) not in sys.path:
        sys.path.insert(0, str(packaging_dir))
    
    try:
        from build_utils.package_checker import _check_req
        from packaging.requirements import Requirement
        has_checker = True
    except ImportError:
        has_checker = False
        print("[UYARI] Bagimlilik kontrol araci yuklenemedi, kurulum oncesi kontrol yapilmayacak")
    
    # 从 requirements 文件读取 PyTorch 源
    primary_index_url = None
    req_file = getattr(args, 'requirements', None)
    if req_file and os.path.exists(req_file):
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('--index-url'):
                        parts = line.split(None, 1)
                        if len(parts) == 2:
                            primary_index_url = parts[1].strip()
                            print(f"Tespit edilen PyTorch kaynagi: {primary_index_url}")
                        break
        except Exception:
            pass
    
    # PyTorch 相关包列表
    pytorch_packages = [
        'torch', 'torchvision', 'torchaudio', 'xformers',
        'pytorch-triton', 'pytorch-triton-rocm', 'pytorch-triton-xpu',
        'nvidia-cublas', 'nvidia-cuda', 'nvidia-cudnn', 'nvidia-cufft',
        'nvidia-curand', 'nvidia-cusolver', 'nvidia-cusparse', 'nvidia-nccl',
        'nvidia-nvjitlink', 'nvidia-nvtx', 'triton',
    ]
    excluded_packages = ['torchsummary', 'torchmetrics']
    
    def is_pytorch_package(pkg_name):
        """检查是否是需要从 PyTorch 源下载的包"""
        pkg_lower = pkg_name.lower()
        if pkg_lower in excluded_packages:
            return False
        for prefix in pytorch_packages:
            if pkg_lower.startswith(prefix):
                return True
        return False
    
    print(f"Kurulacak toplam: {len(missing_packages)} paket daha")
    print()
    
    # 逐个安装缺失的包
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for i, pkg in enumerate(missing_packages, 1):
        pkg_name = pkg.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].split('@')[0].strip()
        
        # 安装前检查包是否Karsilandi要求
        if has_checker:
            try:
                req = Requirement(pkg)
                if _check_req(req):
                    print(f"[{i}/{len(missing_packages)}] {pkg_name} zaten kurulu, atlaniyor")
                    skip_count += 1
                    continue
            except Exception:
                pass  # 检查失败，继续安装
        
        print(f"[{i}/{len(missing_packages)}] Kuruluyor: {pkg_name}...")
        
        try:
            # 检查是否是 PyTorch 相关包
            if is_pytorch_package(pkg_name) and primary_index_url:
                # 使用 PyTorch 源安装，忽略版本锁定安装最新版
                print(f"    (PyTorch kaynagi kullaniliyor)")
                parsed = urllib.parse.urlparse(primary_index_url)
                trusted_host = f'--trusted-host {parsed.hostname}' if parsed.hostname else ''
                # 只用包名，不带版本号
                cmd = f'"{python}" -m pip install "{pkg_name}" --index-url {primary_index_url} {trusted_host} --prefer-binary --disable-pip-version-check'
                result = subprocess.run(cmd, shell=True, env=os.environ)
                if result.returncode != 0:
                    raise RuntimeError(f"Kurulum basarisiz, donus kodu: {result.returncode}")
            else:
                # 普通包，使用 run_pip（支持镜像源回退）
                run_pip(f'install "{pkg}"', pkg_name)
            
            success_count += 1
        except Exception as e:
            print(f"[BASARISIZ] {pkg_name}: {e}")
            fail_count += 1
    
    print()
    print("=" * 40)
    if skip_count > 0:
        print(f"Kurulum tamamlandi: Basarili {success_count} paket, atlanan {skip_count} paket, basarisiz {fail_count} paket")
    else:
        print(f"Kurulum tamamlandi: Basarili {success_count} paket, basarisiz {fail_count} paket")
    print("=" * 40)
    
    return fail_count == 0


def check_all_updates():
    """检查所有更新（代码+依赖）并返回检查结果"""
    ensure_git_safe_directory()
    print()
    print("=" * 40)
    print("正在检查所有更新...")
    print("=" * 40)
    print()
    
    # 1. 检查代码版本和提交
    print("[1/2] Kod surumu kontrol ediliyor...")
    version_file = PATH_ROOT / "packaging" / "VERSION"
    try:
        if version_file.exists():
            current_version = version_file.read_text(encoding='utf-8').strip()
        else:
            current_version = "unknown"
    except Exception:
        current_version = "unknown"
    
    # fetch远程
    try:
        subprocess.run([git, 'fetch', 'origin'], capture_output=True, check=False, timeout=10)
    except Exception:
        pass
    
    # 获取远程版本
    try:
        result = subprocess.run(
            [git, 'show', 'origin/main:packaging/VERSION'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        if result.returncode == 0:
            remote_version = result.stdout.strip()
        else:
            remote_version = "unknown"
    except Exception:
        remote_version = "unknown"
    
    # 获取本地和远程的 commit hash
    try:
        local_commit = subprocess.run(
            [git, 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        ).stdout.strip()
    except Exception:
        local_commit = "unknown"
    
    try:
        remote_commit = subprocess.run(
            [git, 'rev-parse', 'origin/main'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        ).stdout.strip()
    except Exception:
        remote_commit = "unknown"
    
    # 判断是否Guncelleme gerekli：版本号不同 或 提交不同
    version_differs = (current_version != remote_version and remote_version != "unknown")
    commit_differs = (local_commit != remote_commit and remote_commit != "unknown" and local_commit != "unknown")
    code_needs_update = version_differs or commit_differs
    
    print(f"  当前Surum: {current_version}")
    print(f"  远程Surum: {remote_version}")
    print(f"  本地Commit: {local_commit[:8] if local_commit != 'unknown' else 'unknown'}")
    print(f"  远程Commit: {remote_commit[:8] if remote_commit != 'unknown' else 'unknown'}")
    
    if code_needs_update:
        if version_differs:
            print("  状态: [Guncelleme gerekli - surumu不同]")
        else:
            print("  状态: [Guncelleme gerekli - 有新提交]")
    else:
        print("  状态: [Zaten en yeni]")
    
    # 2. 检查依赖
    print()
    print("[2/2] Bagimliliklar kontrol ediliyor...")
    
    # 检测已安装的 PyTorch 类型
    req_file, pytorch_type, detail = get_requirements_file_from_env()
    if req_file:
        print(f"  Tespit edilen PyTorch: {pytorch_type} ({detail})")
        print(f"  依赖文件: {req_file}")
    else:
        print("  PyTorch tespit edilemedi")
        req_file = None
    
    # 检查依赖是否满足
    deps_needs_update = False
    missing_packages = []
    if req_file and os.path.exists(req_file):
        # 导入依赖检查工具
        packaging_dir = PATH_ROOT / 'packaging'
        if str(packaging_dir) not in sys.path:
            sys.path.insert(0, str(packaging_dir))
        
        print("  Bagimlilik butunlugu kontrol ediliyor...")
        try:
            from build_utils.package_checker import check_req_file, get_missing_packages_from_file
            missing_packages = get_missing_packages_from_file(req_file)
            if missing_packages:
                deps_needs_update = True
                print(f"  Durum: [Eksik bagimlilikler var, toplam {len(missing_packages)} paket]")
                # 显示缺失的包（最多显示10个）
                if len(missing_packages) <= 10:
                    for pkg in missing_packages:
                        pkg_name = pkg.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
                        print(f"    - {pkg_name}")
                else:
                    for pkg in missing_packages[:10]:
                        pkg_name = pkg.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
                        print(f"    - {pkg_name}")
                    print(f"    ... ve {len(missing_packages) - 10} paket daha")
            else:
                print("  Durum: [Bagimliliklar tam]")
        except ImportError:
            print("  Durum: [Kontrol edilemiyor, guncelleme onerilir]")
            deps_needs_update = True
    else:
        print("  Durum: [Kurulum gerekli]")
        deps_needs_update = True
    
    # Kontrol Tamamlandi提示
    print()
    print("=" * 40)
    print("Kontrol Tamamlandi")
    print("=" * 40)
    
    # 汇总结果
    print()
    print("Kontrol Sonuclari:")
    print("=" * 40)
    print(f"代码: {'Guncelleme gerekli' if code_needs_update else 'Zaten en yeni'}")
    print(f"依赖: {'Guncelleme/Kurulum gerekli' if deps_needs_update else 'Karsilandi'}")
    print("=" * 40)
    
    return code_needs_update, deps_needs_update, current_version, remote_version, req_file, missing_packages


def maintenance_menu():
    """维护菜单"""
    print()
    print("=" * 40)
    print("Manga Cevirici - 更新维护工具")
    print("Manga Translator UI - Guncelleme Araci")
    print("=" * 40)
    
    # 创建一个简单的 args 对象用于依赖更新
    class Args:
        def __init__(self):
            self.frozen = False
            self.requirements = 'auto'
            self.reinstall_torch = False
            self.update_deps = False
    
    args = Args()
    
    # 首次显示版本信息
    check_version_info()
    
    while True:
        print()
        print("Islem secin:")
        print("[1] Kodu guncelle (zorla senkronize et)")
        print("[2] Bagimliliklari Guncelle/Kur")
        print("[3] Tam guncelleme (kod + bagimliliklar)")
        print("[4] Onarim modu (zorla senkronize + tum bagimliliklari yeniden kur)")
        print("[5] Surumu yeniden kontrol et")
        print("[6] Cik")
        print()
        
        choice = input("Seciniz (1/2/3/4/5/6): ").strip()
        
        if choice == '1':
            update_code_force()
            input("\n按回车键继续...")
            
        elif choice == '2':
            update_dependencies(args)
            input("\n按回车键继续...")
            
        elif choice == '3':
            # 先做总体检查
            code_needs_update, deps_needs_update, current_ver, remote_ver, req_file, missing_packages = check_all_updates()
            
            print()
            if not code_needs_update and not deps_needs_update:
                print("[BILGI] Kod ve bagimliliklar zaten en yeni, guncelleme gerekmiyor")
                input("\n按回车键继续...")
                continue
            
            # 询问是否继续
            print()
            confirm = input("Tam guncellemeye devam edilsin mi? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("Guncelleme iptal edildi")
                input("\n按回车键继续...")
                continue
            
            print()
            print("=" * 40)
            print("Tam Guncelleme Basliyor")
            print("=" * 40)
            
            # 执行更新
            update_success = True
            
            if code_needs_update:
                print()
                print("[1/2] 更新代码...")
                if not update_code_force(skip_confirm=True):
                    update_success = False
                    print("[HATA] Kod guncellenemedi, bagimliliklar atlaniyor")
            else:
                print()
                print("[1/2] Kod zaten en yeni, atlaniyor")
            
            if update_success and deps_needs_update:
                print()
                print("[2/2] 更新依赖...")
                
                # 代码更新后，重新检查依赖（使用最新的 requirements 文件）
                if code_needs_update:
                    print("重新读取更新后的依赖文件...")
                    _, _, _, _, req_file, missing_packages = check_all_updates()
                
                if req_file:
                    args.requirements = req_file
                # 如果有缺失包列表，只安装缺失的包
                if missing_packages:
                    print(f"只安装缺失的 {len(missing_packages)} paket daha...")
                    update_dependencies_selective(args, missing_packages)
                else:
                    update_dependencies(args)
            elif update_success:
                print()
                print("[2/2] Bagimliliklar karsilandi, atlaniyor")
            
            print()
            if update_success:
                print("=" * 40)
                print("[TAMAM] 完整更新完成")
                print("=" * 40)
            
            input("\n按回车键继续...")
            
        elif choice == '4':
            # Onarim Modu：强制同步代码 + 重装所有依赖
            print()
            print("=" * 40)
            print("Onarim Modu")
            print("=" * 40)
            print()
            print("[UYARI] Bu islem sunlari yapacak:")
            print("  1. Kodu uzak surume zorla senkronize et (yerel degisiklikler silinecek)")
            print("  2. Tum bagimlilik paketlerini kaldir ve yeniden kur")
            print()
            
            confirm = input("Onarima devam edilsin mi? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("Onarim iptal edildi")
                input("\n按回车键继续...")
                continue
            
            print()
            print("=" * 40)
            print("Onarim Basliyor")
            print("=" * 40)
            
            # 1. 强制同步代码
            print()
            print("[1/2] Kod zorla senkronize ediliyor...")
            if not update_code_force(skip_confirm=True):
                print("[HATA] Kod senkronizasyonu basarisiz")
                input("\n按回车键继续...")
                continue
            
            # 2. 重装所有依赖
            print()
            print("[2/2] Tum bagimliliklar yeniden kuruluyor...")
            
            # 检测 PyTorch 类型
            req_file, pytorch_type, detail = get_requirements_file_from_env()
            if not req_file:
                # PyTorch tespit edilemedi，让用户选择
                args.requirements = 'auto'
                print("PyTorch tespit edilemedi, otomatik tespit edilip kurulacak")
            else:
                args.requirements = req_file
                print(f"Tespit edilen PyTorch turu: {pytorch_type} ({detail})")
                print(f"Kullaniliyor: {req_file}")
            
            print()
            print("Tum bagimliliklar kaldiriliyor...")
            
            # 读取 requirements 文件，卸载所有包
            if req_file and os.path.exists(req_file):
                try:
                    packaging_dir = PATH_ROOT / 'packaging'
                    if str(packaging_dir) not in sys.path:
                        sys.path.insert(0, str(packaging_dir))
                    
                    from build_utils.package_checker import load_req_file
                    all_packages = load_req_file(req_file)
                    
                    # 这些包是 launch.py 运行时依赖的，不能卸载
                    # 否则后续的安装操作会失败
                    protected_packages = {
                        'packaging',      # 用于解析 requirements
                        'pip',           # pip 本身
                        'setuptools',    # 安装依赖
                        'wheel',         # 构建 wheel
                    }
                    
                    # 提取包名 - 使用 Requirement 对象解析
                    package_names = []
                    for pkg_str in all_packages:
                        try:
                            # 使用 packaging.requirements.Requirement 解析
                            from packaging.requirements import Requirement
                            req = Requirement(pkg_str)
                            # 使用 name 属性获取规范化的包名
                            pkg_name = req.name
                            if pkg_name:
                                package_names.append(pkg_name)
                        except Exception:
                            # 解析失败，使用简单的字符串分割
                            if '@' in pkg_str:
                                pkg_name = pkg_str.split('@')[0].strip()
                            else:
                                pkg_name = pkg_str.split('==')[0].split('>=')[0].split('<=')[0].split('<')[0].split('>')[0].strip()
                            
                            if '[' in pkg_name:
                                pkg_name = pkg_name.split('[')[0].strip()
                            
                            pkg_name = pkg_name.rstrip(',').strip()
                            
                            if pkg_name:
                                package_names.append(pkg_name)
                    
                    # 过滤掉受保护的包
                    original_count = len(package_names)
                    package_names = [p for p in package_names if p.lower() not in protected_packages]
                    if original_count != len(package_names):
                        print(f"  [跳过] 保留关键包: {', '.join(protected_packages)}")
                    
                    if package_names:
                        print(f"Kaldiriliyor: {len(package_names)} paket daha...")

                        
                        # 分批卸载，每次最多20个包，避免命令行过长
                        batch_size = 20
                        failed_packages = []
                        
                        for i in range(0, len(package_names), batch_size):
                            batch = package_names[i:i+batch_size]
                            batch_str = ' '.join(batch)
                            
                            try:
                                print(f"  Kaldirma grubu {i//batch_size + 1}/{(len(package_names) + batch_size - 1)//batch_size}...")
                                run(f'"{python}" -m pip uninstall {batch_str} -y', f"Kaldiriliyor: {len(batch)} paket daha", "卸载失败", capture_output=False)
                            except Exception as batch_err:
                                print(f"  Toplu kaldirma basarisiz, tek tek kaldirilmaya calisiliyor...")
                                # 批次失败，逐个卸载
                                for pkg in batch:
                                    try:
                                        run(f'"{python}" -m pip uninstall {pkg} -y', f"Kaldiriliyor: {pkg}", "卸载失败", capture_output=False)
                                    except Exception:
                                        failed_packages.append(pkg)
                        
                        if failed_packages:
                            print(f"  [UYARI] {len(failed_packages)} paket daha卸载失败: {', '.join(failed_packages[:5])}")
                            if len(failed_packages) > 5:
                                print(f"         ... ve {len(failed_packages) - 5} paket")
                        else:
                            print("  ✓ Tum paketler kaldirildi")
                        
                        # 清理 pip 缓存
                        print('pip onbellegi temizleniyor...')
                        run(f'"{python}" -m pip cache purge', "Onbellek temizleniyor", "无法Onbellek temizleniyor", capture_output=False)
                except Exception as e:
                    print(f"Bagimliliklar kaldirilirken hata: {e}")
                    print("Kuruluma devam ediliyor...")
            
            # 强制重装
            args.reinstall_torch = True
            args.update_deps = True
            args.frozen = False
            
            print()
            print("Tum bagimliliklar yeniden kuruluyor...")
            try:
                prepare_environment(args)
                print()
                print("=" * 40)
                print("[TAMAM] 修复完成")
                print("=" * 40)
            except Exception as e:
                print()
                print("=" * 40)
                print(f"[HATA] Onarim basarisiz: {e}")
                print("=" * 40)
            
            input("\n按回车键继续...")
            
        elif choice == '5':
            check_version_info()
            
        elif choice == '6':
            print()
            print("Guncelleme aracinden cik")
            break
            
        else:
            print("Gecersiz secim")


def launch_ui(args):
    """启动UI界面"""
    if args.ui == 'qt':
        # 新版 Qt UI (推荐)
        from desktop_qt_ui.main import main as qt_main
        qt_main()
    elif args.ui == 'customtkinter':
        # 旧版 CustomTkinter UI
        import importlib
        desktop_ui = importlib.import_module('desktop-ui.main')
        desktop_ui.main_ui()
    else:
        # 默认使用新版 Qt UI
        from desktop_qt_ui.main import main as qt_main
        qt_main()


def launch_cli(args):
    """启动命令行版本"""
    import manga_translator.__main__ as cli_main
    # 传递参数给命令行版本
    cli_main.main()


def main():
    """主函数"""
    # 检查Python版本
    if not is_python_version_valid():
        sys.exit(1)

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Manga Ceviri Baslatic Betigi')
    parser.add_argument("--update", action='store_true', help="启动前检查并自动更新")
    parser.add_argument("--frozen", action='store_true', help="跳过依赖检查(打包版本)")
    parser.add_argument("--install-deps-only", action='store_true', help="仅安装依赖,不启动UI")
    parser.add_argument("--reinstall-torch", action='store_true', help="重新安装PyTorch")
    parser.add_argument("--update-deps", action='store_true', help="更新依赖到最新版本(步骤4使用)")
    parser.add_argument("--requirements", default='auto', help="依赖文件路径 (auto=自动选择, 或指定 requirements_gpu.txt/requirements_cpu.txt)")
    parser.add_argument("--ui", choices=['qt', 'tk'], default='tk', help="选择UI框架: qt(PyQt6) 或 tk(CustomTkinter)")
    parser.add_argument("--cli", action='store_true', help="使用命令行模式")
    parser.add_argument("--verbose", action='store_true', help="显示详细日志")
    parser.add_argument("--maintenance", action='store_true', help="启动更新维护菜单")
    
    args, unknown = parser.parse_known_args()
    
    # 如果是维护模式，直接进入维护菜单
    if args.maintenance:
        # 切换到项目根目录
        os.chdir(PATH_ROOT)
        maintenance_menu()
        return

    # 显示版本信息
    commit = commit_hash()
    print('=' * 60)
    print('Manga Cevirici - Manga Translator UI')
    print('=' * 60)
    print(f'Surum: {VERSION}')
    print(f'Dal: {BRANCH}')
    print(f'Commit: {commit[:8]}')
    print(f'Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
    print(f'Python yolu: {sys.executable}')
    print('=' * 60)

    # 切换到项目根目录 (launch.py 在 packaging/ 下,需要切换到父目录)
    APP_DIR = PATH_ROOT
    os.chdir(APP_DIR)

    # 更新检查
    if update_repository(args):
        return  # 更新后会自动重启

    # 准备环境
    print('\n正在检查依赖...')
    use_amd_pytorch, amd_gfx_version = prepare_environment(args)

    # 如果只是安装依赖,则退出
    if args.install_deps_only:
        print('\n依赖安装完成!')
        
        # 如果是 AMD GPU 且安装了 requirements_amd.txt，提示 PyTorch 状态
        if use_amd_pytorch and amd_gfx_version:
            print('\n✓ AMD ROCm PyTorch kuruldu/guncellendi')
            print(f'  gfx Surum: {amd_gfx_version}')
        
        return

    # 启动应用
    print('\n正在启动应用...\n')
    try:
        if args.cli:
            launch_cli(args)
        else:
            launch_ui(args)
    except KeyboardInterrupt:
        print('\n\n用户取消')
        sys.exit(0)
    except Exception as e:
        print(f'\n错误: {e}')
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


