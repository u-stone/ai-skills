/**
 * my_engine_api.h — 完整的 C ABI 头文件示例
 *
 * 演示了本 Skill 中所有模式：
 *   - opaque handle 创建/销毁
 *   - 错误码 + last-error 查询
 *   - 回调 + void* context
 *   - 数组/buffer 的输入输出
 *   - 版本查询
 *   - 结构体版本兼容
 *   - 线程安全标注
 */

#ifndef MY_ENGINE_API_H
#define MY_ENGINE_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================
 *  不透明 Handle
 * ============================================================ */
typedef struct MyEngine_t   MyEngine;
typedef struct MyScene_t    MyScene;

/* ============================================================
 *  错误码
 * ============================================================ */
#define MY_ENGINE_OK             0
#define MY_ENGINE_ERR_FILE       1
#define MY_ENGINE_ERR_MEMORY     2
#define MY_ENGINE_ERR_PARAM      3
#define MY_ENGINE_ERR_TIMEOUT    4

/* ============================================================
 *  回调类型
 * ============================================================ */

/** 日志回调。context 由调用者注册时传入，C 层原样传回。 */
typedef void (*MyLogCallback)(const char* message,
                              int severity,
                              void* context);

/** 进度回调。progress 范围 0.0–1.0 */
typedef void (*MyProgressCallback)(float progress,
                                   void* context);

/* ============================================================
 *  配置结构体（带版本字段，支持未来扩展）
 * ============================================================ */
typedef struct {
    size_t struct_size;       /* 调用者填入 sizeof(MyEngineConfig) */
    int    width;
    int    height;
    int    max_fps;
    const char* window_title;
    /* 未来添加字段时旧调用者不受影响 */
} MyEngineConfig;

/* ============================================================
 *  版本
 * ============================================================ */

/** 返回 API 版本号：MAJOR*10000 + MINOR*100 + PATCH */
int my_engine_get_api_version(void);

/* ============================================================
 *  Engine 生命周期
 * ============================================================ */

/** 创建引擎实例。
 *  [thread] 必须在主线程调用。
 *  [error]  失败返回 NULL；调用 my_engine_get_last_error 获取详情。
 */
MyEngine* my_engine_create(const MyEngineConfig* config);

/** 销毁引擎实例。
 *  [thread] 必须在主线程调用；销毁前确保所有回调已注销。
 */
void my_engine_destroy(MyEngine* engine);

/* ============================================================
 *  Error 查询（per-instance）
 * ============================================================ */

/** 获取最后一次错误码。
 *  [thread] thread-safe。
 */
int my_engine_get_last_error_code(const MyEngine* engine);

/** 获取最后一次错误信息（只读，生命周期跟随 engine）。
 *  [thread] thread-safe。
 */
const char* my_engine_get_last_error_message(const MyEngine* engine);

/* ============================================================
 *  Engine 操作
 * ============================================================ */

/** 推进一帧。
 *  [thread] 主线程。
 *  [return] 0 = 成功；非 0 = 错误码
 */
int my_engine_tick(MyEngine* engine, float delta_time);

/** 加载场景。
 *  [thread] 主线程。
 *  [return] 0 = 成功；非 0 = 错误码
 */
int my_engine_load_scene(MyEngine* engine, const char* scene_path);

/* ============================================================
 *  Getter（只读查询）
 * ============================================================ */

/** 获取当前 FPS。
 *  [thread] thread-safe。
 */
int my_engine_get_fps(const MyEngine* engine);

/** 获取应用名称（只读指针，engine 存活期内有效）。
 *  [thread] thread-safe。
 */
const char* my_engine_get_app_name(const MyEngine* engine);

/* ============================================================
 *  Setter
 * ============================================================ */

int my_engine_set_max_fps(MyEngine* engine, int max_fps);

/* ============================================================
 *  回调注册 / 注销
 * ============================================================ */

/** 注册日志回调。返回 token 用于注销。
 *  [thread] 主线程。
 *  [return] >=0 = token；<0 = 错误码
 */
int my_engine_set_log_callback(MyEngine* engine,
                               MyLogCallback callback,
                               void* context);

/** 注销日志回调。
 *  [thread] 主线程。
 */
void my_engine_remove_log_callback(MyEngine* engine, int token);

/* ============================================================
 *  Buffer 输出：先查大小，再获取数据
 * ============================================================ */

/** 获取日志缓冲区所需大小（含 null terminator）。
 *  [thread] thread-safe。
 *  [return] 所需字节数
 */
size_t my_engine_get_logs_size(const MyEngine* engine);

/** 获取日志内容。
 *  [thread] thread-safe。
 *  [return] 实际写入字节数（≤ buffer_size）
 */
size_t my_engine_get_logs(MyEngine* engine,
                          char* buffer,
                          size_t buffer_size);

/* ============================================================
 *  Scene 子对象（通过 Engine 创建，独立 destroy）
 * ============================================================ */

MyScene* my_scene_create(MyEngine* engine, const char* name);
void     my_scene_destroy(MyScene* scene);

#ifdef __cplusplus
}
#endif

#endif /* MY_ENGINE_API_H */
