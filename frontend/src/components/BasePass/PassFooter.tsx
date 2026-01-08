interface PassFooterProps {
  entityName?: string
  entityColor: string
  context?: string
  showBranding?: boolean
}

/**
 * Standardized Pass Footer Component
 * 
 * Provides consistent branding footer across all passes with:
 * - Entity-themed background
 * - Subtle pattern overlays
 * - Company branding
 */
export function PassFooter({
  entityName = 'Baynunah Group',
  entityColor,
  context = 'Recruitment',
  showBranding = true
}: PassFooterProps) {
  // Determine if this is agriculture entity for pattern variation
  const isAgriculture = entityName.toLowerCase().includes('agriculture')

  return (
    <div 
      className="px-4 py-3 text-center flex-shrink-0 border-t border-slate-100/50 relative overflow-hidden"
      style={{ backgroundColor: `${entityColor}06` }}
    >
      {/* Subtle pattern for entity theme */}
      <div 
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: isAgriculture
            ? 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M30 0c8.284 0 15 6.716 15 15 0 8.284-6.716 15-15 15-8.284 0-15-6.716-15-15C15 6.716 21.716 0 30 0zm0 45c8.284 0 15 6.716 15 15H15c0-8.284 6.716-15 15-15z\' fill=\'%2300bf63\' fill-opacity=\'1\' fill-rule=\'evenodd\'/%3E%3C/svg%3E")'
            : 'url("data:image/svg+xml,%3Csvg width=\'52\' height=\'26\' viewBox=\'0 0 52 26\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z\' fill=\'%2300B0F0\' fill-opacity=\'1\' fill-rule=\'evenodd\'/%3E%3C/svg%3E")',
          backgroundSize: '30px 30px'
        }}
      />
      
      {showBranding && (
        <span className="text-[10px] text-slate-500 font-medium relative z-10">
          {context}: <span style={{ color: entityColor }} className="font-semibold">{entityName}</span>
        </span>
      )}
    </div>
  )
}
