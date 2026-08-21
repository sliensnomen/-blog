"use client";

import { motion } from 'framer-motion';

interface MusicSectionProps {
  formData: any;
  handleUpdate: (field: string, value: any) => void;
  pushToQueue: (label: string, key?: string, value?: any) => void;
  musicDetails: Record<string, any>;
  queryMusic: () => void;
  queryLoading: boolean;
  queryResult: any;
  confirmAddMusic: () => void;
  removeSong: (index: number) => void;
}

export default function MusicSection({
  formData,
  handleUpdate,
  pushToQueue,
  musicDetails,
  queryMusic,
  queryLoading,
  queryResult,
  confirmAddMusic,
  removeSong
}: MusicSectionProps) {
  const ids = formData.cloudMusicIds || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="bg-white/40 dark:bg-slate-900/40 backdrop-blur-xl border border-white/50 dark:border-slate-800/50 rounded-3xl p-6 shadow-xl"
    >
      <h2 className="text-xl font-black text-slate-900 dark:text-white mb-6 flex items-center gap-2">
        <span>🎵</span> 音乐播放设置
      </h2>

      <div className="space-y-6">
        {/* 当前播放列表 */}
        <div>
          <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">当前播放列表 ({ids.length})</h3>
          {ids.length === 0 ? (
            <div className="text-sm text-slate-500 dark:text-slate-400 bg-white/30 dark:bg-slate-800/30 rounded-2xl p-4 text-center">
              还没有添加歌曲，请在下方添加网易云音乐 ID
            </div>
          ) : (
            <div className="space-y-2">
              {ids.map((id: string, index: number) => {
                const info = musicDetails[id];
                return (
                  <div
                    key={`${id}-${index}`}
                    className="flex items-center justify-between bg-white/50 dark:bg-slate-800/50 rounded-2xl p-3 border border-white/40 dark:border-white/10"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <span className="text-xs font-black text-indigo-500 w-6 h-6 flex items-center justify-center bg-indigo-100 dark:bg-indigo-900/30 rounded-full shrink-0">
                        {index + 1}
                      </span>
                      <div className="min-w-0">
                        <p className="text-sm font-bold text-slate-800 dark:text-slate-200 truncate">
                          {info?.name || `歌曲 ID: ${id}`}
                        </p>
                        <p className="text-[10px] text-slate-500 dark:text-slate-400 truncate">
                          {info?.artists ? `🎤 ${info.artists}` : '未知艺术家'} · ID: {id}
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => removeSong(index)}
                      className="ml-2 px-3 py-1.5 text-xs font-bold text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-colors shrink-0"
                    >
                      移除
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* 添加新歌曲 */}
        <div className="bg-white/30 dark:bg-slate-800/30 rounded-2xl p-4 space-y-4">
          <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300">添加网易云音乐</h3>

          <div className="flex gap-3">
            <input
              type="text"
              value={formData.newMusicId || ''}
              onChange={(e) => handleUpdate('newMusicId', e.target.value)}
              placeholder="输入网易云音乐歌曲 ID"
              className="flex-1 px-4 py-3 rounded-xl bg-white/60 dark:bg-slate-800/60 border border-white/50 dark:border-slate-700/50 text-sm font-medium text-slate-800 dark:text-slate-200 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            />
            <button
              onClick={queryMusic}
              disabled={queryLoading}
              className="px-5 py-3 bg-indigo-500 hover:bg-indigo-600 disabled:bg-indigo-300 text-white text-sm font-bold rounded-xl transition-colors shrink-0"
            >
              {queryLoading ? '查询中...' : '查询'}
            </button>
          </div>

          {queryResult && !queryResult.error && (
            <div className="flex items-center justify-between bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800/50 rounded-2xl p-4">
              <div className="min-w-0">
                <p className="text-sm font-bold text-green-800 dark:text-green-200 truncate">{queryResult.name}</p>
                <p className="text-[10px] text-green-600 dark:text-green-400">{queryResult.artists} · ID: {queryResult.id}</p>
              </div>
              <button
                onClick={confirmAddMusic}
                className="ml-3 px-4 py-2 bg-green-500 hover:bg-green-600 text-white text-xs font-bold rounded-xl transition-colors shrink-0"
              >
                添加
              </button>
            </div>
          )}
        </div>

        {/* 暂存按钮 */}
        <button
          onClick={() => pushToQueue('音乐播放列表', 'cloudMusicIds', formData.cloudMusicIds)}
          className="w-full py-3 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl transition-colors"
        >
          🎵 暂存播放列表变更
        </button>

        <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-relaxed">
          💡 提示：网易云音乐 ID 可以在歌曲分享链接中找到。例如链接
          <code className="mx-1 px-1.5 py-0.5 bg-slate-200 dark:bg-slate-700 rounded text-slate-700 dark:text-slate-300">music.163.com/song?id=123456</code>
          中的 123456 就是歌曲 ID。
        </p>
      </div>
    </motion.div>
  );
}
