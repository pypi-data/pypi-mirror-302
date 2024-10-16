# ProxySDK

ProxySDK là một giải pháp proxy xoay dân cư cho các dự án tại Việt Nam, đặc biệt phù hợp cho MMO và Airdrop.

## Nội Dung

- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [API](#api)
- [Đóng góp](#đóng-góp)
- [Giấy phép](#giấy-phép)

## Giới thiệu

ProxySDK cung cấp các tính năng chính như quản lý proxy, xoay IP theo tỉnh, và tích hợp dễ dàng vào các dự án hiện có.

## Cài đặt

Cài đặt với `pip`:

```bash
pip install proxy-residential-sdk
```

## Sử dụng

Hướng dẫn cách sử dụng dự án. Dưới đây là một ví dụ mã nguồn:

```python
from proxy_residential_sdk import ProxySDK

sdk = ProxySDK("https://vinproxy.net", "YOUR_API_KEY")
provinces = sdk.get_provinces()
print(provinces)
```

## API

ProxySDK cung cấp các API sau:

### Lấy danh sách tỉnh

- **Phương thức**: `get_provinces(search_text: str = None)`
- **Mô tả**: Trả về danh sách các tỉnh thành có sẵn proxy.
- **Tham số**:
  - `search_text` (tùy chọn): Chuỗi tìm kiếm để lọc danh sách tỉnh.

### Lấy IP mới

- **Phương thức**: `get_new_ip(proxy_key: str, province_id: int = None)`
- **Mô tả**: Lấy một IP mới từ proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy.
  - `province_id` (tùy chọn): ID của tỉnh cần lấy IP.

### Lấy IP hiện tại

- **Phương thức**: `get_current_ip(proxy_key: str)`
- **Mô tả**: Lấy thông tin IP hiện tại của proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy.

### Xóa IP cũ

- **Phương thức**: `remove_old_ip(proxy_key: str)`
- **Mô tả**: Xóa IP cũ của proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy.

### Lấy danh sách khóa

- **Phương thức**: `get_key_list()`
- **Mô tả**: Lấy danh sách các khóa proxy của người dùng.

### Lấy chi tiết khóa

- **Phương thức**: `get_key_detail(proxy_key: str)`
- **Mô tả**: Lấy thông tin chi tiết của một khóa proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy cần lấy thông tin.

### Mua khóa mới

- **Phương thức**: `buy_new_key(buy_key_dto: any)`
- **Mô tả**: Thực hiện giao dịch mua khóa proxy mới.
- **Tham số**:
  - `buy_key_dto`: Đối tượng chứa thông tin mua khóa mới.

### Gia hạn khóa

- **Phương thức**: `renew_key(renew_key_dto: any)`
- **Mô tả**: Gia hạn một khóa proxy hiện có.
- **Tham số**:
  - `renewKeyDto`: Đối tượng chứa thông tin gia hạn khóa.

### Xóa khóa

- **Phương thức**: `remove_key(proxy_key: str)`
- **Mô tả**: Xóa một khóa proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy cần xóa.

### Lấy thông tin người dùng

- **Phương thức**: `get_user_info()`
- **Mô tả**: Lấy thông tin của người dùng hiện tại.

## Đóng góp

Chúng tôi rất hoan nghênh mọi đóng góp cho ProxySDK. Nếu bạn muốn đóng góp, vui lòng làm theo các bước sau:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit các thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
