"""
音乐相关 API：通过第三方 Meting 服务查询网易云音乐详情
"""
import httpx
from fastapi import APIRouter

router = APIRouter()

METING_API_BASE = "https://api.injahow.cn/meting/"


@router.get("/query/{song_id}")
async def query_netease_song(song_id: str):
    """
    查询网易云音乐歌曲信息
    """
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            url = f"{METING_API_BASE}?server=netease&type=song&id={song_id}"
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if isinstance(data, list) and len(data) > 0:
                song = data[0]
                return {
                    "success": True,
                    "data": {
                        "id": song.get("id"),
                        "name": song.get("name"),
                        "artists": song.get("artist"),
                        "album": song.get("album"),
                        "pic": song.get("pic"),
                        "url": song.get("url"),
                        "lrc": song.get("lrc")
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "未找到歌曲信息或 API 返回为空"
                }
    except httpx.TimeoutException:
        return {
            "success": False,
            "message": "查询音乐 API 超时"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"查询失败: {str(e)}"
        }
