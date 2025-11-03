'use client';

interface DashboardWidgetProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: string;
  color: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  href?: string;
}

export default function DashboardWidget({
  title,
  value,
  subtitle,
  icon,
  color,
  trend,
  href
}: DashboardWidgetProps) {
  const Widget = href ? 'a' : 'div';
  const widgetProps = href ? { href, className: `block ${color} bg-opacity-10 p-6 rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer` } : { className: `${color} bg-opacity-10 p-6 rounded-lg shadow-md` };

  return (
    <Widget {...widgetProps}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{icon}</span>
            <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          </div>
          <div className="mt-3">
            <div className={`text-3xl font-bold ${color.replace('bg-', 'text-')}`}>
              {value}
            </div>
            {subtitle && (
              <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
            )}
          </div>
          {trend && (
            <div className="mt-2 flex items-center">
              <span className={`text-sm font-medium ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
              </span>
              <span className="ml-2 text-sm text-gray-500">vs last week</span>
            </div>
          )}
        </div>
      </div>
    </Widget>
  );
}
