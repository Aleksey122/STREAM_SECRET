#[unsafe(no_mangle)]
pub extern "C" fn get_system_status() -> *const i8 {
    "SYSTEM_READY_SECURE\0".as_ptr() as *const i8
}
